$(document).ready(
    function (){
        let counter = 1
        let removeButtons = $('#remove-button')
        let addButton = $('#add-button')
        let submitButton = $('#submit-button')

        addButton.click(function(e){
            e.preventDefault()
            let inputs = $('#inputs')
            let newInputContainer = $("<div class='input-container'></div>")
            let newInput = $(`<input id='input-${counter}' name='input-${counter}' type='text'>`)
            let newRemoveButton = $("<button id='remove-button'>Remove</button>")
            inputs.append(newInputContainer.append(newInput).append(newRemoveButton))
            counter += 1
        })

        
        $(document).on('click', '#remove-button', function(e){
            e.preventDefault()
            $(this).parent().remove()
        })

        submitButton.click(function(e){
            e.preventDefault()
            let formData = $('#dynamic-input').serializeArray()
            console.log(formData)

            $.ajax({
                url: '/form-submit',
                method: 'post',
                dataType: 'json',
                data: formData,
                success: function(response){
                    console.log(response)
                    console.log('success')
                    if(response.redirectURL){
                        window.location.href = response.redirectURL
                    }
                },
                error: function(r, s, e){
                    console.log('error', r, s, e)
                }
            })
        })
    }
)