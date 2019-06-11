addEventListener('click', function(ev) 
{
    var sender = ev.srcElement; 
    var data_container;
    var url;
    var success_msg;
    var send_data = {};
    var success_func;
    var error_func = function(error) { console.log(error); };
    var isRequestCall = false;
    //обновляем основные данные
    //кнопка "сохранить" в settings-list-1
    if (sender.id == 'push-base-settings') 
    {
        isRequestCall = true;
        data_container = document.getElementById('settings-list-1');
        url = '/set_base_userdata';
        success_msg = 'Вы обновили основные данные о себе.';
        error_func = function(error) {
            console.log(json_data);
            console.log(error);
            alert('Ошибка при отправлении запроса');
        };
    }
    if (sender.id == 'change-password-btn') 
    {
        data_container = document.getElementById('settings-list-2');
        PasswordIsCorrect(this.document.getElementById('actual-password').value, function(response)
        {
            if (response['check_result'])
            {
                isRequestCall = true;
                send_data['new_password'] = this.document.getElementById('new-password').value;
                var json_data = JSON.stringify(send_data);
                $.ajax({
                    type: "POST",
                    url: '/change_password',
                    contentType: "application/json",
                    data: json_data,
                    success: function(response) {
                        console.log(response);
                        alert('Вы успешно обновили пароль.');
                    },
                    error: function(error) {
                        error_func(error);
                    }
                });
            }
            else
                alert('Вы неправильно ввели текущий пароль.');
        });
    }
    if (sender.id.includes('delete-user-'))
    {
        isRequestCall = true;
        var user_id = sender.id.split('-')[2];
        send_data['id'] = user_id;
        url = '/delete_user';
        success_msg = 'Пользователь удалён.';
        error_func = function(error) {
            console.log(json_data);
            console.log(error);
            alert('Ошибка при отправлении запроса');
        };
    }
    if (sender.id == 'add-code-template')
    {
        isRequestCall = true;
        data_container = document.getElementById('add-code-templ-container');
        url = '/add_code_template';
        success_msg = 'Фрагмент кода добавлен.';
        error_func = function(error) {
            console.log(json_data);
            console.log(error);
            alert('Ошибка при отправлении запроса');
        };
    }
    if (HasClass(sender, 'pic-delete'))
    {
        isRequestCall = true;
        url = '/delete_photo'
        success_func = function(response)
        {
            document.getElementById('avatar-photo-img').src = response['photo_url'];
        };
        error_func = function(error) {
            console.log(json_data);
            console.log(error);
            alert('Не удалось изменить фото профиля. Подробности в консоли.');
        };
    }
    //данный код выполняется в случае если достоверно известно, что
    //click произошел с целью отправки данных на сервер
    if (isRequestCall)
    {
        if (data_container)
        {
            for (var child of data_container.children)
            {
                for (var elem of child.getElementsByTagName('*'))
                {
                    if (elem.nodeName == 'INPUT' || elem.nodeName == 'SELECT' || elem.nodeName == 'TEXTAREA') 
                        send_data[elem.name] = elem.value;
                }
            }
        }
        var json_data = JSON.stringify(send_data);
        
        $.ajax({
            type: "POST",
            url: url,
            contentType: "application/json",
            data: json_data,
            success: function(response) {
                console.log(response);
                if (success_msg)
                    alert(success_msg);
                success_func(response);
            },
            error: function(error) {
                error_func(error);
            }
        });
    }
});

function PasswordIsCorrect(value, func)
{
    var json_data = JSON.stringify({
        current_password: value
    });
    var resp;
    var request = $.ajax({
        type: "POST",
        url: "/get_password_check_result",
        contentType: "application/json",
        data: json_data,
        success: function(response) {
            resp = response;
        },
        error: function(error) {
            alert('Ошибка проверки пароля на сервере.');
        }
    });
    request.done(function()
    {
        func(resp);
    });
}