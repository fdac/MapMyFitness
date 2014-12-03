setwd("~/Documents/Class/Grad/2014Fall/FDAC/MapMyFitness/")

# read in data
data <- read.csv("workouts.csv", header = TRUE, stringsAsFactors = FALSE, fileEncoding = "UTF-8", na.strings = "", row.names = NULL)
str(data)
summary(data)

length(unique(data$userId)) # number of users
data$active_time_total <- as.numeric(data$active_time_total)

# drop observations missing is_verified
data <- data[!is.na(data$is_verified),]

# convert response to 0 for not verified, 1 for verified workout
data$is_verified <- ifelse(data$is_verified == "True", 1,0)
head(data$is_verified)
data$is_verified <- factor(data$is_verified)
table(data$is_verified)

# check missingness on all variables
sapply(data, function(x) round(sum(is.na(x))/length(x),2))

# number of workouts per user
nbrWorkouts <- aggregate(data$userId, by = list(data$userId), length)
summary(nbrWorkouts[,2])
nbrWorkouts[which.max(nbrWorkouts[,2]),]
head(nbrWorkouts[order(nbrWorkouts[,2], decreasing = TRUE),], 20)

library(dplyr)
nbrWorkouts <- 
  data %>%
  group_by(userId) %>%
  summarise(workouts = n()) %>%
  arrange(desc(workouts))


summary(data)
# clean up outliers and weird shit (e.g. negative metabolic_energy_expenditure)
data <- data[data$active_time_total <= quantile(data$active_time_total, probs = 0.995, na.rm = TRUE),]
data <- data[data$distance_total <= quantile(data$distance_total, probs = 0.995, na.rm = TRUE),]
# data <- data[data$speed_max <= quantile(data$speed_max, probs = 0.995, na.rm = TRUE),]
# trimming the extreme values off speed_max gets rid of almost all android observations, which is interesting
data <- data[data$steps_total <= quantile(data$steps_total, probs = 0.995, na.rm = TRUE),]
data <- data[data$speed_avg <= quantile(data$speed_avg, probs = 0.995, na.rm = TRUE),]
data <- data[data$elapsed_time_total <= quantile(data$elapsed_time_total, probs = 0.995, na.rm = TRUE),]
data <- data[data$metabolic_energy_total <= quantile(data$metabolic_energy_total, probs = 0.995, na.rm = TRUE),]

data <- data[data$metabolic_energy_total > 0,]

# create android-iphone data
android <- data[grep("android", data$source, ignore.case = TRUE),]
iphone <-  data[grep("iphone", data$source, ignore.case = TRUE),]
android.iphone <- rbind(android, iphone)
rm(android, iphone)

android.iphone$is.android <- grepl("android", android.iphone$source, ignore.case = TRUE)
android.iphone$is.android <- as.numeric(android.iphone$is.android)

# create model to try to predict android vs. iPhone
mod.1 <- glm(is.android ~ active_time_total + distance_total + speed_avg + elapsed_time_total + metabolic_energy_total,
             data = android.iphone,
             family = binomial)
summary(mod.1)

# removing mullticollinearity with active_time_total, distance_total, and speed_avg
mod.2 <- glm(is.android ~ distance_total + speed_avg + elapsed_time_total + metabolic_energy_total,
             data = android.iphone,
             family = binomial)
summary(mod.2)

# transform coefficients to odds
exp(summary(mod.1)$coeff[,1])



# try modeling is_verified

# remove rows with missing values
data_complete <- data[complete.cases(data),]

# convert userId to character
data$userId <- as.character(data$userId)

# get character variables
char.vars <- sapply(data, is.character)

# subset data for only numeric variables
num.data <- data[,!char.vars]
names(num.data)
# check missing values
sapply(num.data, function(x) round(sum(is.na(x))/length(x), 2))
summary(num.data)
  # many outliers and missing values

# resolve outliers for active_time_total
quantile(num.data$active_time_total, probs = seq(0.94, 0.99, 0.01), na.rm = TRUE)
active.99pct <- quantile(num.data$active_time_total, probs = 0.99, na.rm = TRUE)
num.data <- num.data[num.data$active_time_total <= active.99pct &
                     num.data$active_time_total > 0,]

# resolve outlier for other vars
quantiles <- lapply(num.data[,-1], quantile, probs = seq(0.94, 0.99, 0.01), na.rm = TRUE)
quantiles <- Reduce(function(x,y) rbind(x,y), quantiles)
row.names(quantiles) <- names(num.data)[2:length(num.data)]
quantiles <- data.frame(quantiles)



num.data.complete <- num.data[complete.cases(num.data),]
num.data.complete <- num.data.complete[num.data.complete$active_time_total <=
                                         quantile(num.data.complete$active_time_total, probs = 0.99),]
num.data.complete <- num.data.complete[num.data.complete$distance_total <=
                                         quantile(num.data.complete$distance_total, probs = 0.99),]
num.data.complete <- num.data.complete[num.data.complete$speed_max <=
                                         quantile(num.data.complete$speed_max, probs = 0.99),]
num.data.complete <- num.data.complete[num.data.complete$steps_total <=
                                         quantile(num.data.complete$steps_total, probs = 0.99),]
num.data.complete <- num.data.complete[num.data.complete$speed_avg <=
                                         quantile(num.data.complete$speed_avg, probs = 0.99),]
num.data.complete <- num.data.complete[num.data.complete$elapsed_time_total <=
                                         quantile(num.data.complete$elapsed_time_total, probs = 0.99),]
num.data.complete <- num.data.complete[num.data.complete$metabolic_energy_total <=
                                         quantile(num.data.complete$metabolic_energy_total, probs = 0.99),]
num.data.complete <- num.data.complete[num.data.complete$metabolic_energy_total > 0,]

summary(num.data.complete$speed_max[num.data.complete$is_verified == 0])


devices <- sort(unique(data$source))


# logistic regression on is_verified
mod0 <- glm(is_verified ~ distance_total + speed_avg + metabolic_energy_total, 
            data = num.data.complete, family = binomial)


# regression for metabolic energy
mod.3 <- glm(metabolic_energy_total ~ distance_total + speed_avg + elapsed_time_total + factor(is_verified),
             data = num.data.complete)
options(scipen=999)
summary(mod.3)

mod.4 <- glm(metabolic_energy_total ~ distance_total + speed_avg + factor(is_verified),
             data = num.data.complete)
summary(mod.4)

mod.5 <- lm(metabolic_energy_total ~ distance_total + speed_avg + factor(is_verified),
             data = num.data.complete)
summary(mod.5)

#Look at the Variation Inflation Factors
require(car)
vif(mod.5)

#Look at the quartiles and histogram of energy
summary(num.data.complete$metabolic_energy_total)
hist(num.data.complete$metabolic_energy_total)
hist(log(num.data.complete$metabolic_energy_total+100000))

#Log transform of energy of mod.5
mod.6 <- lm(log(metabolic_energy_total+1e5) ~ log(distance_total) + log(speed_avg) + factor(is_verified),
            data = num.data.complete)
summary(mod.6)

#Predict distance from time
mod.7 <- lm(log(distance_total) ~ log(active_time_total) + factor(is_verified),
            data = num.data.complete)
summary(mod.7)
anova(mod.7)

library(ggplot2)
plot(num.data.complete$distance_total, num.data.complete$metabolic_energy_total)

p <- ggplot(data = num.data.complete, aes(x=distance_total, y=metabolic_energy_total, color = is_verified, alpha = 1/50))
p <- p + geom_point()
p


