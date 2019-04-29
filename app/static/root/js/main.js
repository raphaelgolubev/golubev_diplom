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
        if (!(stc.hasAttribute('NoStartAnimation')))
        {
            stc.style.cssText += 'transition: unset;';
            stc.style.cssText += 'transform: translate(-50%, -50%) scale(' + scaling + ');';
            stc.style.cssText += 'transition: transform 0.5s cubic-bezier(0.075, 0.82, 0.165, 1) 1s';
        }

        var grid_right = document.getElementsByClassName('grid-item-right');
        var grid_left = document.getElementsByClassName('grid-item-left');

        stc.addEventListener('click', function tutorstart() {
            circ_medium.style.cssText += "transition: transform 0.75s cubic-bezier(0.09,-0.22, 0.99,-0.71);";
            circ_large.style.cssText += "transition: transform 0.75s cubic-bezier(0.09,-0.22, 0.99,-0.71) 0.25s;";

            for (var elem of fadeUp_elements) elem.classList.add('fadeUp-start-state');

            fadeUp_elements[0].addEventListener('transitionend', function after() {
                circ_medium.classList.add('circ-start-state');
                circ_large.classList.add('circ-start-state');

                circ_medium.addEventListener('transitionend', function after() {

                    stc.style.cssText += "transition: border-radius 0.75s ease, transform 0.75s ease 1s;";
                    stc.style.cssText += "border-radius: 0;";
                    stc.style.cssText += "transform: translate(-500%, -300%) rotate(0deg);";
                    circ_medium.removeEventListener('transitionend', after);
                })

                fadeUp_elements[0].removeEventListener('transitionend', after);
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
            stc.addEventListener('transitionend', function after() {
                for (var elem of fadeUp_elements)
                {
                    elem.classList.remove('fadeUp-start-state');
                }
                fadeUp_elements[0].addEventListener('transitionend', function after() {
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
            var settings_list = document.querySelectorAll('.info-block')[0];
            var func = function(evt)
            {
                document.getElementsByClassName('test-box')[0].scrollTop = 0;

                var settings_page = getElementsByAttribute('nostartanimation', 'full-page')[0];

                //название
                var pagename = settings_page.children[0];
                pagename.innerHTML = evt.srcElement.innerHTML;

                //"вернуться назад"
                var goback = settings_page.children[1];
                goback.addEventListener('click', function()
                {
                    settings_page.addEventListener('transitionend', function after()
                    {
                        starter.classList.remove('fadeUp-start-state');
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
            for (var item of settings_list.children) item.addEventListener('click', func);
        }
    }
}
