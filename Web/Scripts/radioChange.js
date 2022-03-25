    
    
$(document).ready(function(){  
    $('input[type=radio][name=algorithm]').change(function(){
        if(this.value=="RandomForestRegressor"){
            $('#RandomForestBlock').show()
            $('#SVRBlock').hide()
            $('#DecissionTreeBlock').hide()
        }else if(this.value=="SVR"){
            $('#RandomForestBlock').hide()
            $('#SVRBlock').show()
            $('#DecissionTreeBlock').hide()
        }else{
            $('#RandomForestBlock').hide()
            $('#SVRBlock').hide()
            $('#DecissionTreeBlock').show() 
        }
    });
});