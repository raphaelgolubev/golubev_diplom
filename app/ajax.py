from app import app, db
import os
from models import User, Profile, BaseSettings, CodeTemplate
from flask_login import current_user
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from werkzeug.urls import url_parse
import json

@app.route('/set_base_userdata', methods=['GET', 'POST'])
def set_base_userdata():
    if request.is_json:
        content = request.get_json()
        username_set = content['username-set']
        email_set = content['email-set']
        country_set = content['country-set']
        city_set = content['city-set']
        contact_set = content['contact-set']
        projects_set = content['projects-set']
        program_langs_set = content['programLangs-set']

        current_user.profile.base_settings.username = username_set
        current_user.email = email_set
        current_user.profile.base_settings.country = country_set
        current_user.profile.base_settings.city = city_set
        current_user.profile.base_settings.contact = contact_set
        current_user.profile.base_settings.projects = projects_set
        current_user.profile.base_settings.programming_langs = program_langs_set

        db.session.commit()
        return jsonify({"content":content})

    return jsonify({"Ответ":"Это не JSON"})

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.is_json:
        content = request.get_json()
        user_id = int(content['id'])
        for user in User.query.all():
            if user.id == user_id:
                db.session.delete(user.profile.base_settings)
                db.session.delete(user.profile)
                db.session.delete(user)
        db.session.commit()
        return jsonify({"content":content})
    return jsonify({"Ответ":"Это не JSON"})

@app.route('/add_code_template', methods=['GET', 'POST'])
def add_code_template():
    if request.is_json:
        content = request.get_json()
        code = content['templ-code']
        lang = content['templ-lang']
        name = content['templ-name']
        short = content['templ-shortname']
        tags = content['templ-tags']

        new_templ = CodeTemplate(name=name, tags=tags, lang=lang,
        short_name=short, code=code)
        current_user.profile.templates.append(new_templ)
        db.session.commit()
        return jsonify({"content":content})
    return jsonify({"Ответ":"Это не JSON"})