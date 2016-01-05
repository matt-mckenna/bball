
#install.packages('xts')
library(xts)
library(dygraphs)


setwd("~/bball/retire/data")

kobe = read.csv('kobe.csv', header=T)
dunc = read.csv('dunc.csv', header=T)
pp = read.csv('pp.csv', header=T)
mj = read.csv('mj.csv', header=T)
stock = read.csv('stock.csv', header=T)
mal = read.csv('mal.csv', header=T)
pip = read.csv('pip.csv', header=T)


plot(y=kobe$eff, x=kobe$inx)
#kobe$year=as.numeric(substr(dat$SEASON_ID,2,5))
#kobepat = filter (kobe, filter = c(1/8, 1/4, 1/4, 1/4, 1/8), sides=2)
#duncpat = filter (dunc, filter = c(1/8, 1/4, 1/4, 1/4, 1/8), sides=2)
#pppat =filter (pp, filter = c(1/8, 1/4, 1/4, 1/4, 1/8), sides=2)

#plot (x=kobe$X, y=kobe$eff,type= "b", main = "moving average annual trend")
#lines (trendpattern)
kobesm=smooth.spline(y=kobe$eff, x=kobe$inx)

dunc.sm=smooth.spline(x=dunc$inx, y=dunc$eff)
pp.sm=smooth.spline(x=pp$inx, y=pp$eff)
mj.sm=smooth.spline(x=mj$inx, y=mj$eff)
pip.sm=smooth.spline(x=pip$inx, y=pip$eff)
stock.sm = smooth.spline(x=stock$inx, y=stock$eff)
mal.sm = smooth.spline(x=mal$inx, y=mal$eff)


plot(y=kobe.sm$y, x=kobe.sm$x,col='blue', ylim=c(0,50), type="l", xlab="Games Played", ylab="Player efficiency", lwd=3)
lines(dunc.sm$y, x=dunc.sm$x,col='red',ylim=c(0,50), type="l", lwd=3)
lines(pp.sm$y, x=pp.sm$x,col='black',ylim=c(0,50), type="l", lwd=3)
lines(mj.sm$y, x=mj.sm$x,col='dark green',ylim=c(0,50), type="l", lwd=3)

legend('bottom', legend=c("Kobe", "Tim Duncan", "Paul Pierce", "MJ"),lty=c(1,1,1,1), 
       lwd=c(2.5,2.5), col=c("blue", "red", "black", "dark green"), ce=.85)

plot(y=mal.sm$y, x=mal$X,col='blue', ylim=c(0,50), type="l", xlab="Games Played", ylab="Player Efficiency", lwd=3)

lines(stock.sm$y, x=stock.sm$x,col='red',ylim=c(0,50), type="l", lwd=3)
lines(pip.sm$y, x=pip.sm$x,col='black',ylim=c(0,50), type="l", lwd=3)

legend('bottom', legend=c("Mailman", "Stockton", "Scottie"),lty=c(1,1,1), 
       lwd=c(2.5,2.5), col=c("blue", "red", "black"), ce=.85)


