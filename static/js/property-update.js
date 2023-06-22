let blankForm = document.querySelector("#blank-form");
const formsetContainer = document.querySelector("#formset-container");
const addBtn = document.querySelector("#add-btn");
const managementForm = document.querySelector("#id_form-TOTAL_FORMS");

function setupCheckboxListeners() {
    const checkboxes = formsetContainer.querySelectorAll('input[name*="is_feature"]');
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

// detect new added delete buttons actions
const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach((mutation) => {
        setupCheckboxListeners()

        let deleteBtns = mutation.target.querySelectorAll('.remove-btn')
        deleteBtns.forEach(btn=> {
            btn.addEventListener('click', ()=>{
                let targetForm = btn.parentElement.parentElement
                let lookup = targetForm.querySelector('input[type="hidden"]').id
                let index = parseInt(lookup.split('-')[1]);
                
                if(targetForm.nextElementSibling === null){
                    targetForm.remove()
                    managementForm.value = mutation.target.childNodes.length -3
                }else {
                    for(let i=index+1; i< managementForm.value; i++){
                        let formRegex = new RegExp(`form-${i}-`, 'g');
                        let div =  mutation.target.querySelector(`#id_form-${i}-id`).parentElement
                        div.innerHTML = div.innerHTML.replace(formRegex, `form-${i-1}-`)
                    }
                    targetForm.remove()
                    managementForm.value = mutation.target.childNodes.length -3
                }
            })
        })
    })
});

const config = { childList: true };
observer.observe(formsetContainer, config);


// add more image forms
addBtn.addEventListener('click', (e)=>{
    e.preventDefault();
    const formsetNode = blankForm.cloneNode(true);
    let formNum = parseInt(managementForm.value)
    const formRegex = new RegExp('__prefix__', 'g');
    formsetNode.innerHTML = formsetNode.innerHTML.replace(formRegex, formNum);
    managementForm.value = parseInt(managementForm.value) + 1;
    formsetNode.classList.remove('hidden');
    formsetNode.removeAttribute('id');
    formsetContainer.appendChild(formsetNode);
})

const existingCheckBoxes = formsetContainer.querySelectorAll('input[name*="is_feature"]');
existingCheckBoxes.forEach(box => {
    setupCheckboxListeners();
});
