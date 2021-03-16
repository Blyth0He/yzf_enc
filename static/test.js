$.ajax({
    url:'/encrypt',
    type: 'GET',
    success: function(data){
        console.log(data.result)
    }
});