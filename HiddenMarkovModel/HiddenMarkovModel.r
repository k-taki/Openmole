######## Parameter settings #########

# Hidden states number of HMM
HMMstates=10

# AMEDAS variables
AMEDAS_variable=2
#####################################

# Based on the following webpages:
# http://rstudio-pubs-static.s3.amazonaws.com/2998_ba38dfe6c545468ea0c55892ae8f1202.html

# Set working directory
setwd("/Users/masa_funabashi/Dropbox/Programs_R/Openmole/HiddenMarkovModel")

# Show working directory
wd <- getwd()
cat("Current working dir: ", wd)

# Read AMEDAS tsv data file
#AMEDAS <- read.table("kishouchou_data/kishouchou_Alldata2011Tokyo.txt", header=TRUE, sep="\t")
#AMEDAS <- read.table("kishouchou_data/kishouchou_Alldata2012Tokyo.txt", header=TRUE, sep="\t")
AMEDAS_2011_2012 <- read.csv("kishouchou_data/dataTokyo2011-2012_1header.csv")
AMEDAS_2013 <- read.csv("kishouchou_data/dataTokyo2013_1header.csv")
AMEDAS <- rbind(AMEDAS_2011_2012,AMEDAS_2013)

#日付の処理：strptime()関数を使って、日付指定の文字列をPOSIXltオブジェクトへ変換
YMD_AMEDAS <- strptime(AMEDAS$Y.M.D, "%Y/%m/%d", tz="")
#グラフに日付を表示するには、グラフを表示させたままの状態で、以下のコマンドを打つ必要がある。
#r <- as.POSIXct(round(range(YMD), "days"))
#axis.POSIXct(1, at=seq(r[1],r[2], by=”1 week”), format=”%m/%d”)

print(AMEDAS)


# Fit AMEDAS variable with HMM　with univariate gaussian distributions
x <- AMEDAS[,AMEDAS_variable]

# Fit time series x with HMM
library("RHmm")
hmm.fitted <- HMMFit(x, dis = "NORMAL", nStates = HMMstates)

# フォワードα・バックワードβ再帰による確率計算
fb <- forwardBackward(hmm.fitted, x)


# gammaの時系列プロット(各隠れ状態にいる推定確率のプロット)
dev.new()
# margin setting for 2 y-axis plot
default.par <- par()
mai <- par()$mai
mai[4] <- mai[1]
par(mai = mai)
# Plot probability of each hidden state
color=sample(rainbow(HMMstates))
legend <- ""
for(state in 1:HMMstates){
	plot(YMD_AMEDAS,fb$Gamma[, state], type = "l", main = "Probability being in Hidden States", xlab = "Date", ylab = "Probability", 
lwd = 3, col=color[state],ylim=c(0,1))
	par(new=T)  # 上書き指定 
	if(state==1) legend <- paste("State", state, "probability")
	else	legend <- append(legend, paste("State", state, "probability"))
}
# 実際の時系列を重ねる
plot(YMD_AMEDAS,x, type = "l", lwd = 3, xlab = "Date", ylab = "", axes = FALSE, col="black")
axis(4)
mtext("AMEDAS Data", side = 4, line = 3)
#par(default.par)
legend <- append(legend, "AMEDAS Data")
# 日付の表示
r <- as.POSIXct(round(range(YMD_AMEDAS), "days"))
axis.POSIXct(1, at=seq(r[1],r[2], by="1 month"), format="%m/%d")
# legendの表示
legend(x = "topleft", rev(legend), lty=matrix(1,1,HMMstates), col=append("black",color)) # head(fb$Gamma)で見ると、state1が最後の列にあるので、stateのナンバリングが列番号とは逆になっているのでrev(legend)が必要
#　図の保存
dev.copy(png,paste('Plot1_Date_VS_HiddenStatesProbability_AMEDASvariable=',AMEDAS_variable,'HMMstates=',HMMstates,'.png'), width = 1000, height = 400)
dev.off()


# 解析モジュールTo do:
# 過去のデータを元にHMMモデルを学習させると、今どの隠れ状態にいるかがViterviのアルゴリズムから推定出来るので、季節遷移の予測になる。

