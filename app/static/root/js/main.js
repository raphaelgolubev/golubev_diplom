function FadeIn(fade_elements, direction = 'vertical')
{
    if (direction.toLowerCase() == 'vertical')
    {
        for (var elem of fade_elements)
        {
            if (!(elem.hasAttribute('NoStartAnimation')))
                elem.classList.remove('fadeUp-start-state');
        }
    }
}

function getElementsByAttribute(attribute, classname = null, value = null)
{
    var matchingElements = [];
    var allElements = document.getElementsByTagName('*');
    for (var i = 0, n = allElements.length; i < n; i++)
    {
        if (allElements[i].getAttribute(attribute) !== null)
        {
            if (value)
            {
                var att = allElements[i].getAttribute(attribute);
                if (att.toLowerCase() == value.toLowerCase())
                    matchingElements.push(allElements[i]);
            }
            else if (classname)
            {
                for (var classitem of allElements[i].classList)
                {
                    if (classitem.toLowerCase() == classname.toLowerCase())
                        matchingElements.push(allElements[i]);
                }
            }
            else
                matchingElements.push(allElements[i]);
        }
    }
    return matchingElements;
}

window.onload = async function(evt) {
    if (evt.target.title.toLowerCase().includes('главная'))
    {
        var fadeUp_elements = document.querySelectorAll('.fadeUp-start-state');
        var circ_medium = document.getElementsByClassName('circ-medium')[0];
        var circ_large = document.getElementsByClassName('circ-large')[0];

        var test_box = document.getElementsByClassName('test-box')[0];
        var stc = document.getElementsByClassName('start-circle')[0];
        var scaling = (test_box.offsetWidth / stc.offsetWidth)+3;
        //стартовая анимация кружочков
        if (!(stc.hasAttribute('NoStartAnimation')))
        {
            stc.style.cssText += 'transition: unset;';
            stc.style.cssText += 'transform: translate(-50%, -50%) scale(' + scaling + ');';
            stc.style.cssText += 'transition: transform 0.5s cubic-bezier(0.075, 0.82, 0.165, 1) 1s';
            stc.addEventListener('transitionend', function after() 
            {
                var search_icon = stc.childNodes[0].nodeName == 'IMG' ? stc.childNodes[0] : stc.childNodes[1];
                search_icon.style.cssText += 'opacity: 1;';
                stc.removeEventListener('transitionend', after);
            });
        }
        //нажимаем на кружочек с иконкой поиска
        stc.addEventListener('click', function searchshow() {
            stc.style.cssText += 'transition: transform 0.5s ease';
            circ_medium.style.cssText += 'transition: all 0.8s ease';
            circ_large.style.cssText += 'transition: all 0.8s ease 0.2s';

            circ_medium.classList.add('circ-start-state');
            circ_large.classList.add('circ-start-state');
            circ_large.addEventListener('transitionend', function after() 
            {
                var search_icon = stc.childNodes[0].nodeName == 'IMG' ? stc.childNodes[0] : stc.childNodes[1];
                search_icon.style.cssText += 'opacity: 0;';
                //создали строку поиска и задали scaleX(0)
                var search_input = document.createElement('input');
                search_input.type = 'text';
                search_input.placeholder = 'Пример: шаблон html';
                search_input.style.cssText += 'position: fixed; top: 50%; left: 50%; font-size: 150%; width: 75%;';
                search_input.style.cssText += 'transform: translate(-50%,-50%) scaleX(0);' +
                //задаем переход 
                'transition: transform 0.5s ease;';
                stc.parentElement.appendChild(search_input);

                search_icon.addEventListener('transitionend', function after_search_icon_hide() 
                {
                    //после того как иконка поиска исчезла
                    //удаляем img с иконкой
                    search_icon.parentElement.removeChild(search_icon);
                    //убираем кружок
                    stc.style.cssText += 'transform: translate(-50%, -50%) scale(0);';
                    //задаем scaleX(1) для анимации
                    search_input.style.cssText += 'transform: translate(-50%,-50%) scaleX(1);';
                    search_icon.removeEventListener('transitionend', after_search_icon_hide);
                });

                circ_large.removeEventListener('transitionend', after);
            });
        });

        if (stc.hasAttribute('NoStartAnimation'))
        {
            for (var elem of fadeUp_elements)
            {
                elem.classList.remove('fadeUp-start-state');
            }
            fadeUp_elements[0].addEventListener('transitionend', function after() {
                circ_medium.classList.remove('circ-start-state');
                circ_large.classList.remove('circ-start-state');
                fadeUp_elements[0].removeEventListener('transitionend', after);
            });
        }
        else
        {
            stc.classList.remove('stc-start-state');
            stc.style.cssText = '';
            stc.addEventListener('transitionend', function after() 
            {
                for (var elem of fadeUp_elements)
                {
                    elem.classList.remove('fadeUp-start-state');
                }
                fadeUp_elements[0].addEventListener('transitionend', function after()
                {
                    circ_medium.classList.remove('circ-start-state');
                    circ_large.classList.remove('circ-start-state');
                    fadeUp_elements[0].removeEventListener('transitionend', after);

                });
                stc.removeEventListener('transitionend', after);
            })
        }
    }
    else {
        var fadeUp_elements = document.querySelectorAll('.fadeUp-start-state');
        FadeIn(fadeUp_elements)

        if (document.querySelectorAll('.info-block')[0])
        {
            var setting_UL = document.querySelectorAll('.info-block')[0];
            
            var func = function(evt)
            {
                var current_settings_list = evt.srcElement.getAttribute('settings-list');
                document.getElementById('settings-list-' + current_settings_list).style.cssText += 'display: block';
                document.getElementsByClassName('test-box')[0].scrollTop = 0;
                
                var settings_page = getElementsByAttribute('nostartanimation', 'full-page')[0];
                settings_page.style.cssText += 'pointer-events: all;';
                //название
                var pagename = document.getElementsByClassName('setting-name')[0];
                pagename.innerHTML = evt.srcElement.innerHTML;

                //"вернуться назад"
                var goback = document.getElementsByClassName('setting-subname')[0];
                goback.addEventListener('click', function()
                {
                    settings_page.addEventListener('transitionend', function after()
                    {
                        starter.classList.remove('fadeUp-start-state');
                        settings_page.style.cssText += 'pointer-events: none;';

                        for(var child of settings_page.children)
                        {
                            if (child.id.includes('settings-list-'))
                            {
                                child.style.cssText += 'display: none';
                            }
                        }

                        settings_page.removeEventListener('transitionend', after);
                    });
                    settings_page.classList.add('fadeUp-start-state');
                });

                //страница профиля
                var starter = document.getElementById('starter');
                starter.addEventListener('transitionend', function after()
                {
                    settings_page.classList.remove('fadeUp-start-state');
                    starter.removeEventListener('transitionend', after);
                });
                starter.classList.add('fadeUp-start-state');
            }
            for (var item of setting_UL.children) item.addEventListener('click', func);
        }
    }
}
