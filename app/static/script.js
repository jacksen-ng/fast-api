document.addEventListener('DOMContentLoaded', function() {
    var buttons = {
        'showFunction1Button': 'function1Form',
        'showFunction2Button': 'function2Form',
        'showFunction3Button': 'function3Form'
    };

    Object.keys(buttons).forEach(function(buttonId) {
        var button = document.getElementById(buttonId);
        var formId = buttons[buttonId];
        var form = document.getElementById(formId);
        
        button.addEventListener('click', function() {
            if (form.style.display === 'none' || form.style.display === '') {
                form.style.display = 'block';
            } else {
                form.style.display = 'none';
            }
        });
    });

    var functionForms = ['function1Form', 'function2Form', 'function3Form'];
    functionForms.forEach(function(formId) {
        var form = document.getElementById(formId);
        var result = null;

        if (formId === 'function1Form') {
            result = form.getAttribute('data-result');
        } else if (formId === 'function2Form') {
            result = form.getAttribute('data-bubble-result');
        } else if (formId === 'function3Form') {
            result = form.getAttribute('data-image-result');
        }

        if (result && result.trim() !== '') {
            form.style.display = 'block';
        }
    });
});
