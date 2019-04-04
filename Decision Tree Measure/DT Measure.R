# Gain
get_gain = function(d, p, ratio){
  # d: class ratio in D
  # p: positive probability in each cluster
  # ratio: ratio of each cluster
  infoD = get_info(d)
  infoDj = get_info(p)
  gain = infoD-sum(ratio*infoDj, na.rm=T)
  return(gain)
}
## information gain
get_info = function(p){
  info = -(p*(log2(p))+(1-p)*log2(1-p))
  return(info)
}

# Gain ratio
get_gain_ratio = function(d, p, ratio){
  gain = get_gain(d,p,ratio)
  split = get_split_info(ratio)
  return(gain/split)
}
## split info
get_split_info = function(ratio){
  return(-sum(ratio*log2(ratio)))
}

# Gini Index
get_gini = function(d,p,ratio){
  giniD = get_gini_index(d)
  giniA = sum(ratio*get_gini_index(p))
  return(giniD-giniA)
}
get_gini_index = function(p){
  ps = c(p, (1-p))
  return(1-sum(ps^2))
}

# Age
d = 5/8
p = c(2/3, 3/3, 0)
ratio = c(3/8, 3/8, 2/8)
get_gain(d,p, ratio)
get_gain_ratio(d,p,ratio)
get_gini(d,p,ratio)
# 0.360

# Gender
p = c(4/5, 1/5)
ratio = c(5/8, 3/8)
get_gain(d,p, ratio)
get_gain_ratio(d,p,ratio)
get_gini(d,p,ratio)

# 0.232

# Education
p = c(1, 1/2, 0, 1/2)
ratio = c(3/8, 2/8, 1/8, 2/8)
get_gain(d,p, ratio)
get_gain_ratio(d,p,ratio)
get_gini(d,p,ratio)


