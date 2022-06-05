$(document).ready(function(){
    $('.algselection').on('change', function(){
        if(this.value=="RandomForestRegressor"){
            $('#RandomForestRegressor').show()
            $('#SVR').hide()
            $('#DecissionTree').hide()
            $('#algorithmRF').prop('selectedIndex', 0);
        }else if(this.value=="SVR"){
            $('#RandomForestRegressor').hide()
            $('#SVR').show()
            $('#DecissionTree').hide()
            $('#algorithmSVR').prop('selectedIndex', 1);
        }else{
            $('#RandomForestRegressor').hide()
            $('#SVR').hide()
            $('#DecissionTree').show()
            $('#algorithmDT').prop('selectedIndex', 2);
        }
    });
});