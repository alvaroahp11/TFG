
#Limpio todo
rm(list = ls())


#Cargo nortest y car
library(nortest)
library(car)

#Defino funcion que aplica los contrastes
aplicaContrastes <- function(datos1,datos2){

	#Inicializo variables
	w<-0
	t<-0
	lev<-0

	#Contrastes de normalidad de Lilliefors
	lil1<-lillie.test(datos1)$p.value
	lil2<-lillie.test(datos2)$p.value
	
	#Si los datos no son normales, aplico el contraste de Wilcoxon
	if (lil1<0.05 || lil2<0.05){ 

		mediana1<-median(datos1)
		mediana2<-median(datos2)
		#H1: mediana1 < mediana2
		if(mediana1<mediana2){
			w=wilcox.test(datos1,datos2,alternative="less")$p.value 
		}else{
			w=wilcox.test(datos2,datos1,alternative="less")$p.value
		}


		if (w<0.01){
			if (mediana1<mediana2){return("--")}else{return("++")}			
		}else{
			if (w<0.05){
				if (mediana1<mediana2){return("-")}else{return("+")}
			}else{return("=")}
		}

	}else{ #En caso de haber normalidad

		datoslevene<-c(datos1,datos2)                                             
    		media1<-mean(datos1)
		media2<-mean(datos2)
		#crea el vector de agrupacion
		agrupalevene<-c(rep(1,length(datos1)),rep(2,length(datos2)))

    		lev<-leveneTest(datoslevene,agrupalevene)$Pr[1]
 
   		if (lev<0.05){
			#caso heterocedasticidad (Welch)
			#H1: media1 < media2
			if(media1<media2){
				t<-t.test(datos1,datos2,alternative="less")$p.value
			}else{
				t<-t.test(datos2,datos1,alternative="less")$p.value
			}

			if (t<0.01){
				if (media1<media2){return("--")}else{return("++")}
			}else{
				if (t<0.05){
					if (media1<media2){return("-")}else{return("+")}
				}else{return("=")}
			}

    		}else{

			#caso homocedasticidad (T-test)
			#H1: media1 < media2
			if(media1<media2){
				t<-t.test(datos1,datos2,alternative="less",var.equal=TRUE)$p.value
			}else{
				t<-t.test(datos2,datos1,alternative="less",var.equal=TRUE)$p.value
			}
			if (t<0.01){
				if (media1<media2){return("--")}else{return("++")}
			}else{
				if (t<0.05){
					if (media1<media2){return("-")}else{return("+")}
				}else{return("=")}
			}
    		} #If Levene
    } #If Normalidad
} #Funcion


# Este segmento del c?digo es el que se encarga de cargar datos y hacer contrastes

# Archivos a procesar terminados en TXT. Esta cadena se puede cambiar por otra mejor (GREP)
fuentesdatos<-list.files(pattern="_")
numfuentes<-length(fuentesdatos)
resultados<-matrix(nrow=numfuentes,ncol=numfuentes,dimnames=list(fuentesdatos,fuentesdatos))

#Leo las estructuras de datos y las meto en vectores con el nombre del archivo
for (i in fuentesdatos){
	eval(parse(text=paste(i,"<-scan(i)")))
}

#Guardo los resultados de los contrastes
indice<-c(1:numfuentes)
for (i in indice){
	for (j in indice){
		if(i>j){
			resultados[i,j]=eval(parse(text=paste("aplicaContrastes(",fuentesdatos[i],",",fuentesdatos[j],")")))
		}else{resultados[i,j]="NA"}
	}
}
print(resultados)

			eval(parse(text=paste("aplicaContrastes(",fuentesdatos[1],",",fuentesdatos[2],")")))

#Guardo tabla de estadisticos
estadisticos<-matrix(nrow=numfuentes,ncol=5,dimnames=list(fuentesdatos,list("Media","Mediana","Var.","Max","Min")))
for (i in indice){
	estadisticos[i,1]<-eval(parse(text=paste("mean(",fuentesdatos[i],")")))
	estadisticos[i,2]<-eval(parse(text=paste("median(",fuentesdatos[i],")")))
	estadisticos[i,3]<-eval(parse(text=paste("var(",fuentesdatos[i],")")))
	estadisticos[i,4]<-eval(parse(text=paste("max(",fuentesdatos[i],")")))
	estadisticos[i,5]<-eval(parse(text=paste("min(",fuentesdatos[i],")")))
}
print(estadisticos)

#Vuelco a disco. Hay varias formas de hacerlo
write.table(resultados, file = "Contrastes", append = TRUE, sep = "\t")
#unlink("Resultados")

write.table(estadisticos, file = "Estadisticos", append = TRUE, sep = "\t")
#unlink("Estadisticos")




