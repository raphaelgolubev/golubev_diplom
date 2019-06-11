addEventListener('click', function(ev) 
{
    var sender = ev.srcElement; 
    var data_container;
    var url;
    var success_msg;
    var send_data = {};
    var isRequestCall = false;
    //обновляем основные данные
    //кнопка "сохранить" в settings-list-1
    if (sender.id == 'push-base-settings') 
    {
        isRequestCall = true;
        data_container = document.getElementById('settings-list-1');
        url = '/set_base_userdata';
        success_msg = 'Вы обновили основные данные о себе.';
    }
    if (sender.id.includes('delete-user-'))
    {
        isRequestCall = true;
        var user_id = sender.id.split('-')[2];
        send_data['id'] = user_id;
        url = '/delete_user';
        success_msg = 'Пользователь удалён.';
    }
    if (sender.id == 'add-code-template')
    {
        isRequestCall = true;
        data_container = document.getElementById('add-code-templ-container');
        url = '/add_code_template';
        success_msg = 'Фрагмент кода добавлен.';
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
            type: 'POST',
            success: function(response) {
                console.log(response);
                alert(success_msg);
            },
            error: function(error) {
                console.log(json_data);
                console.log(error);
                alert('Ошибка при отправлении запроса');
            }
        });
    }
});