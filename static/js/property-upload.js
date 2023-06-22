const managementForm = document.querySelector('#id_form-TOTAL_FORMS')
const blankForm = document.querySelector('#empty-formset')
const targetContainer = document.querySelector('#target-container')
const addFormBtn = document.querySelector('#add-more-btn')


function setupCheckboxListeners() {
    const checkboxes = targetContainer.querySelectorAll('input[name*="is_feature"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            checkboxes.forEach(cb => {
                if (cb !== checkbox) {
                    cb.checked = false;
                }
            });
        });
    });
}

const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach((mutation) => {
        setupCheckboxListeners()
       
        let deleteBtns = mutation.target.querySelectorAll('.delete')
        deleteBtns.forEach(btn=> {
            btn.addEventListener('click', ()=>{
                let targetForm = btn.parentElement.parentElement
                let lookup = targetForm.querySelector('input[type="hidden"]').id
                let index = parseInt(lookup.split('-')[1]);
                
                if(targetForm.nextElementSibling === null){
                    targetForm.remove()
                    managementForm.value = mutation.target.childNodes.length -2
                }else {
                    for(let i=index+1; i< managementForm.value; i++){
                        let formRegex = new RegExp(`form-${i}-`, 'g');
                        let div =  mutation.target.querySelector(`#id_form-${i}-id`).parentElement
                        div.innerHTML = div.innerHTML.replace(formRegex, `form-${i-1}-`)
                    }
                    targetForm.remove()
                    managementForm.value = mutation.target.childNodes.length -2
                }
            })
        })
    })
});

const config = { childList: true };
observer.observe(targetContainer, config);


// add forms
addFormBtn.addEventListener('click', (e)=>{
    e.preventDefault()
    const formsetNode = blankForm.cloneNode(true);
    let formNum = parseInt(managementForm.value)
    const formRegex = new RegExp('__prefix__', 'g');
    formsetNode.innerHTML = formsetNode.innerHTML.replace(formRegex, formNum);
    managementForm.value = parseInt(managementForm.value) + 1;
    formsetNode.classList.remove('hidden');
    formsetNode.removeAttribute('id');
    targetContainer.appendChild(formsetNode);
    
    targetContainer.appendChild(formsetNode);   

})
