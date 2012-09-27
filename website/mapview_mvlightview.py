# -*- coding: utf-8 -*-

'''mvlightview
'''

import json
import web


render = web.template.render('./templates/')

urls = ('/mapweibo/mapview/mvlightview', )

class handler():
    def GET(self):
        form = web.input(idlist=None)
        if form.idlist != None:        
            return render.mvlightview()
    
