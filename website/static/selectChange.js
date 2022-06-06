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
    //
    // const $form = document.querySelector('#RandomForestRegressor')
    // const $form2 = document.querySelector('#SVR')
    // const $form3 = document.querySelector('#DecissionTree')
    //
    // $form.addEventListener('submit', (event)=>{
    //     event.preventDefault()
    //     const randomForest = new FormData($form)
    //     randomForest.set('n_estimators', parseInt(randomForest.get('n_estimators')))
    //     debugger
    //
    // })
    // $form2.addEventListener('submit', (event)=>{
    //     event.preventDefault()
    //     const svr = new FormData($form2)
    //
    // })
    // $form3.addEventListener('submit', (event)=>{
    //     event.preventDefault()
    //     const decissionTree = new FormData($form3)
    // })
});

