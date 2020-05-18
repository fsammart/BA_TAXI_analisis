 # library
library(ggplot2)
library(plotly)
library(wesanderson)

cbp1 <- c("#999999", "#E69F00", "#56B4E9", "#009E73",
          "#0072B2", "#D55E00", "#CC79A7")


weekday_groupby <- read.csv("http://fsammart.github.io/BA_TAXI_analisis/bataxi_groupby_weekday.csv" , fileEncoding = "utf-8", skipNul = TRUE )
weekday_groupby$dia_de_semana <- factor(weekday_groupby$dia_de_semana,levels = c("Sunday", "Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday"),
                                        labels=c("Domingo", "Lunes", "Martes","Miércoles","Jueves","Viernes","Sabado"))
weekday_groupby$momento_dia <- factor(weekday_groupby$momento_dia ,levels = c("Madrugada", "Noche", "Tarde", "Mediodia","Mañana"), labels=c("22-6 hs", "18-22 hs", "14-18 hs", "10-14 hs","6-10 hs"))
# Stacked
p <- ggplot(weekday_groupby, aes(fill=momento_dia, y=count, x=dia_de_semana)) + 
  geom_bar(position = position_stack(), stat = "identity", width = .7) +
  geom_text(aes(label = count), position = position_stack(vjust = .5), color="white", size=3.5) +
  ggtitle("Trafico semanal") +
  labs(x = "Día de la Semana" , y = "Cantidad de Viajes")+
  scale_fill_manual(name = 'Momento del \nDía' , values = cbp1)


ggplotly(p, tooltip = NULL)