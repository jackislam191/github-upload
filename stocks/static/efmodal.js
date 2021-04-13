//alert

const img = document.getElementById('img');
//save in portfolio modal
const saveBtn = document.getElementById('save-btn');
const saveModalbody = document.getElementById('save-in-database-modal-body');
const savealertBox = document.getElementById('save-alert-box')
//form
const saveEFform = document.getElementById('save-portfolio-form');
const saveEFnameid = document.getElementById('id_name');
const saveEFdescid = document.getElementById('id_description');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

console.log(csrf);
console.log(saveEFform);
console.log(saveEFnameid);
console.log(saveEFdescid);

if (img){
    saveBtn.classList.remove('not-visible')
}
console.log(img);

//output csv modal
saveBtn.addEventListener('click', () =>{
    console.log('clicked');
    img.setAttribute('class', 'w-100')
    saveModalbody.prepend(img);
})

//csv alert 


//save alert 
const saveAlert = (type, msg) => {
    savealertBox.innerHTML =  `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>

    `
}


//save in portfolio modal
saveBtn.addEventListener('click', () =>{
    console.log('clicked');
    img.setAttribute('class', 'w-100')
    saveModalbody.prepend(img);

    saveEFform.addEventListener('submit', e=>{
        e.preventDefault()
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('save_name', saveEFnameid.value)
        formData.append('save_descr', saveEFdescid.value)
        formData.append('image', img.src)

        $.ajax({
            type:'POST',
            url: '/portfolio/save_in_portfolio/',
            data: formData,
            //dataType: "json",
            success: function(data){
                if(data.success == 'Saved!') {
                    saveAlert('success', 'New Efficient Frontier is added!')
                    $('#savemodal').modal('hide')
                }
                else {
                    saveAlert('danger', 'Please check your input value')
                }
 
            },
            error: function(data){
                console.log(error)
                if (data.fail == 'Try again later!'){
                    saveAlert('danger', 'Somethings went wrong! Please try again! later')
                }
            },
            processData: false,
            contentType: false,
        })
    })
})

