library('RANN')
# main function that generates the paths
generate_tad_random = function(hops = 1000, origin = rep(0,3), limit =1, abs_limit = limit * 4 ,scale = 0.1, min_delta=scale, cis=50, warp = NULL){

	central_origin = origin
	tad_loc = data.frame(x = origin[1], y = origin[2], z = origin[3])
	#tad_loc = origin
	current = origin
	pos = data.frame(x=current[1], y=current[2], z=current[3])

	delta = c(0,0,0)
	mem_trail = delta
	
	hop = 1
	iter = 1
	while(hop <= hops){
		if(!is.null(warp)){
			if(hop%%warp == 0){
				valid_warp = FALSE
				warp_jump = 0
				mem_jump = 0
				center_dist = -1
				w_ori = current	
				w_hop = tensor(current, current, limit = limit, scale = 5 * scale)$pos
				while(!valid_warp){
					w_hop = tensor(w_ori, w_hop, limit = limit, scale = 5 * scale)$pos
					center_dist = euclidean_distance(w_hop, central_origin)	
					warp_jump = euclidean_distance(w_hop, current) 
					mem_jump = euclidean_distance(w_hop, mem_trail[nrow(mem_trail), ]) 

					valid_warp= ifelse( 
							warp_jump > 4 * scale &
							mem_jump > 4 * scale &
							center_dist < abs_limit, T, F)
					
				}
				current = w_hop
				origin = w_hop
				message(sprintf("\t hop %s warp dist to abs center %.2f %s", hop, center_dist, abs_limit))
				plot_progress(pos, mem_trail, warp)

				pos = rbind(pos, fhop$pos)
				mem_trail = rbind(mem_trail, memory)
				delta = c(delta, fhop$delta)
				current = fhop$pos
				hop = hop + 1
				#cat(sprintf("\r%.2f\t%s", hop/hops, iter))

			}
		}
		iter = iter +1
		fhop = tensor(origin, current, limit= limit, scale = scale)
		if(hop >=cis){
			memory = memory_centroid(pos[(nrow(pos)-cis):nrow(pos), ])
		} else {
			memory = colMeans(pos) #current + rnorm(3, 0, min_delta)
		}

		#cat(sprintf("last jump was of %.2f", euclidean_distance(fhop$pos, current)))
		#message(sprintf("from the origin %.2f", euclidean_distance(fhop$pos, origin)))
		if(nrow(pos)>0){
			knn = nn2(as.matrix(pos), matrix(fhop$pos, ncol=3, nrow=1), k = nrow(pos))
			knn = knn$nn.dist[1,1] > min_delta *1.52
		}else{
			knn = TRUE
		}
		valid = ifelse(euclidean_distance(fhop$pos, current) >= min_delta &
				euclidean_distance(memory, fhop$pos) >= min_delta *2 &
				knn,T, F)	


		if(valid){
			pos = rbind(pos, fhop$pos)
			mem_trail = rbind(mem_trail, memory)
			delta = c(delta, fhop$delta)
			current = fhop$pos
			hop = hop + 1
			cat(sprintf("\r%.2f%%\t%s", 100*hop/hops, iter))
		}


	}
	cat("\n")

	#path = matrix(pos, ncol=3, byrow=T)
	path = pos 
	colnames(path) = c("x","y","z")
	deltas = matrix(delta, ncol=3, byrow=T)
	colnames(deltas) = c("dx","dy","dz")

	#as.data.frame(cbind(path, deltas))
	#as.data.frame(path)
	list(path=as.data.frame(path), deltas=deltas, mem_trail=mem_trail, cis=cis)
}

# main engine that suggests the next step on a path 
tensor= function(origin=c(0,0,0), current=c(0,0,0), limit = 1, penalty_factor = 0.25, scale = 0.1){
	pf = penalty_factor
	x = current[1]
	y = current[2]
	z = current[3]
	if(euclidean_distance(origin, current) > limit){
		dx = (origin[1] - x) * pf
		dy = (origin[2] - y) * pf
		dz = (origin[3] - z) * pf
		nx = rnorm(1, 0, scale)
		ny = rnorm(1, 0, scale)
		nz = rnorm(1, 0, scale)
		delta = c(nx, ny, nz) + (c(dx,dy,dz) * sapply(c(0,0,0), function(x){ifelse(sign(x)==0, 1, sign(x))}))
	
	} else {
		nx = rnorm(1, 0, scale)
		ny = rnorm(1, 0, scale)
		nz = rnorm(1, 0, scale)
		delta = -c(nx, ny, nz)
	}
	return(list(pos = current + delta, delta=delta))
}
# basic functions
euclidean_distance = function(a, b){
	distance = 0
	if(length(a) != length(b)){
		stop("vectors are not the same length")
	}
	points = rbind(a,b)
	sqrt(sum(apply(points, 2, function(x){diff(x)**2})))

}

memory_centroid = function(a){
	colMeans(a)
}

knn_path = function(tad_list, k=100, len=20, region=20:30){

	end = nrow(tad_list$path)
	start = tad_list$cis + (end*0.1)

	knn = nn2(tad_list$path, tad_list$path, k=100)
	k = c()

	x = sample(start:end, 1)
	i = 1
	while(i <= len){
		x <- knn$nn.idx[x, sample(region, 1)]
		if(!(x %in% k)){
			k = c(k,x)
			i = i+1
		}
	}
	dev.new()
	plot(tad_list$path[k,], t='l')
	return(tad_list$path[k,])
}

dist_3d = function(a,b){
	x = a[1]; y = a[2]; z = a[3]
	xx = b[1]; yy = b[2]; zz = b[3]
	sqrt(sum((x-xx)^2, (y-yy)^2, (z-zz)^2))
}


plot_progress = function(pos, mem_trail, warp = NULL){
	layout(matrix(c(1, 2, 0, 3), ncol = 2, nrow = 2))
	ext_lim = range(c(pos, mem_trail))
	
	n_mem = nrow(mem_trail)
	f_warp = 1:n_mem %% warp == 0

	plot(pos[, 1], pos[, 2], t='l', xlab="X", ylab="Y")
	points(mem_trail[f_warp, 1], mem_trail[f_warp, 2], pch=19, col='red')
	abline(v=mem_trail[n_mem, 1], h=mem_trail[n_mem, 2], col='lightblue', lty=2, lwd=2)

	plot(pos[, 1], pos[, 3], t='l', xlab="X", ylab="Z")
	points(mem_trail[f_warp, 1], mem_trail[f_warp, 3],pch=19, col='red')
	abline(v=mem_trail[n_mem, 1], h=mem_trail[n_mem, 3], col='lightblue', lty=2, lwd=2)

	plot(pos[, 2], pos[, 3], t='l', xlab="Y", ylab="Z")
	points(mem_trail[f_warp, 2], mem_trail[f_warp, 3],pch=19, col='red')
	abline(v=mem_trail[n_mem, 2], h=mem_trail[n_mem, 3], col='lightblue', lty=2, lwd=2)

	
#	plot(mem_trail[,1], mem_trail[,2], t='l', col='red')
#	plot(mem_trail[,2], mem_trail[,3], t='l', col='red')
#	plot(mem_trail[,1], mem_trail[,3], t='l', col='red')

}
