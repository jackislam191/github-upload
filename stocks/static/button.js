const stocksymbolId = document.getElementById('id_stock_symbol');
const stocksharesId = document.getElementById('id_stock_shares');
const stockpriceId = document.getElementById('id_stock_price');
const positionForm = document.getElementById('position-form');
const addBtn = document.getElementById('add-stock-btn');
const alertBox = document.getElementById('alert-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

console.log(csrf)
console.log(stocksymbolId)
console.log(stocksharesId)
console.log(stockpriceId)

addBtn.addEventListener('click', ()=>{
    console.log('clicked!');


    positionForm.addEventListener('submit', e =>{
        e.preventDefault();
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrf);
        formData.append('stock_symbol', stocksymbolId.value);
        formData.append('stock_shares', stocksharesId.value);
        formData.append('stock_price', stockpriceId.value);

        $.ajax({
            type:'POST',
            url: '/quotes/add_to_portfolio/',
            data: formData,
            //dataType: "json",
            success: function(response){
                console.log(response)

            },
            error: function(error){
                console.log(error)
            },
            processData: false,
            contentType: false,
        })
        
    })

})
//CSRF value
//gILrntVyMUHVn9BuhwL6lPQzGOT6uHglBH8PXjhPtE7M3jypo4TmnXFHfNxZwez7