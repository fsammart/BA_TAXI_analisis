library(ggplot2)
library(plotly)

trips = read.csv("http://fsammart.github.io/BA_TAXI_analisis/number-of-trips-per--bataxi-QueryResult.csv" , fileEncoding = "latin1", skipNul = TRUE )

p <- ggplot(trips, aes(x=duration_average, y=trips)) +
    geom_point(color = rgb(0.4,0.4,0.8,0.6)) +
    geom_rug()+
    stat_summary(fun.y=mean, geom="point",color="green3")+
    labs(x = "Duration Avg." , y = "Trips per Driver")

ggplotly(p)
