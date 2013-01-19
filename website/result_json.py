# -*- coding: utf-8 -*-

'''profiling原型界面使用的模拟数据
'''

import web
import json
import csv

urls = ('/profile/result.json', )

class handler():
    def GET(self):
        form = web.input(module=None)
        if form.module:
            if form.module == 'bubble':
                return json.dumps(bubble_result)
            elif form.module == 'graph':
                return json.dumps(graph_result)
            elif form.module == 'hashtags_vis':
                return json.dumps(hashtags_result)
            elif form.module == 'community_pie':
                csv_data = []
                csv_data.append("State,Under 5 Years,5 to 13 Years,14 to 17 Years,18 to 24 Years,25 to 44 Years,45 to 64 Years,65 Years and Over\n")
                for data in community_pie_result:
                    row = [data[0],str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[5]),str(data[6]),str(data[7])]
                    csv_data.append(",".join(row) + "\n")
                return json.dumps(csv_data)
            elif form.module == "personal_keywords_cloud":
                personal_cloud()
            else:
                return json.dumps(bubble_result)
        else:
            return json.dumps(bubble_result)

bubble_result = {"name": "薛蛮子", "children": [{"name": "tags","children":[{"name": "社会","children":[{"name": "#钓鱼岛#", "size": 3938},
                                                                                                 {"name": "#韩德强打人#", "size": 3812}]},
                                                                  {"name": "影视","children":[{"name": "#越来越好#", "size": 3534},
                                                                                               {"name": "#笑傲江湖#", "size": 5731},
                                                                                               {"name": "#隋唐英雄#", "size": 7840},
                                                                                               {"name": "#爱情自有天意#", "size": 5914},
                                                                                               {"name": "#一代宗师#", "size": 3416}]},
                                                                  {"name": "行业","children":[{"name": "#又又Note II#", "size": 3074},
                                                                                            {"name": "#央视曝常州新房积压#", "size": 2074},
                                                                                            {"name": "#善融商务#", "size": 7074},
                                                                                            {"name": "#连锁酒店日成本15元#", "size": 7074}]},
                                                                  {"name": "明星人物","children":[{"name": "#马云将辞阿里CEO#", "size": 3074},
                                                                                            {"name": "#潘长江当姥爷了#", "size": 2074},
                                                                                            {"name": "#微博之夜#", "size": 7074},
                                                                                            {"name": "#刘嘉玲黎姿周慧敏美艳合照#", "size": 7074}]}
                                                                 ]}]}

graph_result = {"nodes":[{"name":"薛蛮子","group":1,"profile_image_url":"0"},
                         {"name":"内分泌顾锋","group":1,"profile_image_url":"1"},
                         {"name":"留几手","group":1,"profile_image_url":"2"},
                         {"name":"妈咪Jane育儿妙方","group":1,"profile_image_url":"3"},
                         {"name":"好友美食","group":1,"profile_image_url":"4"},
                         {"name":"毛高山","group":1,"profile_image_url":"5"},
                         {"name":"管鹏","group":1,"profile_image_url":"6"},
                         {"name":"协和章蓉娅","group":1,"profile_image_url":"7"},
                         {"name":"张遇升","group":1,"profile_image_url":"8"},
                         {"name":"炎黄春秋编辑部","group":1,"profile_image_url":"9"},
                         {"name":"苏家桥","group":1,"profile_image_url":"10"},
                         {"name":"精神科李医生","group":2,"profile_image_url":"11"},
                         {"name":"释源祖庭白马寺","group":2,"profile_image_url":"12"},
                         {"name":"Brad_Pitt","group":3,"profile_image_url":"13"},
                         {"name":"胡泽涛-Henry","group":2,"profile_image_url":"14"},
                         {"name":"姚树坤","group":2,"profile_image_url":"15"},
                         {"name":"瞬间就笑岔气了","group":2,"profile_image_url":"16"},
                         {"name":"口袋悦读","group":3,"profile_image_url":"17"},
                         {"name":"慕容雪村","group":3,"profile_image_url":"18"},
                         {"name":"老树画画","group":3,"profile_image_url":"19"},
                         {"name":"大河网信阳频道吴彦飞","profile_image_url":"20"},
                         {"name":"桔子水晶吴海","group":3,"profile_image_url":"21"},
                         {"name":"谢维冰","group":3,"profile_image_url":"22"},
                         {"name":"社科院杨团","group":3,"profile_image_url":"23"},
                         {"name":"围脖唯美句","group":3,"profile_image_url":"24"},
                         {"name":"参考消息","group":4,"profile_image_url":"25"},
                         {"name":"九个头条","group":4,"profile_image_url":"26"},
                         {"name":"天才小熊猫","group":5,"profile_image_url":"27"},
                         {"name":"赵克罗","group":4,"profile_image_url":"28"},
                         {"name":"泰国苏梅岛自助游指南","group":0,"profile_image_url":"29"},
                         {"name":"苏宁孙为民","group":2,"profile_image_url":"30"},
                         {"name":"马翾","group":3,"profile_image_url":"31"}],
"links":[{"source":0,"target":1,"value":2},{"source":0,"target":2,"value":8},{"source":0,"target":3,"value":10},{"source":0,"target":4,"value":6},
         {"source":0,"target":5,"value":2},{"source":0,"target":6,"value":8},{"source":0,"target":7,"value":10},{"source":0,"target":8,"value":6},
         {"source":0,"target":9,"value":2},{"source":0,"target":10,"value":8},{"source":0,"target":11,"value":10},{"source":0,"target":12,"value":6},
         {"source":0,"target":13,"value":2},{"source":0,"target":14,"value":8},{"source":0,"target":15,"value":10},{"source":0,"target":16,"value":6},
         {"source":0,"target":17,"value":2},{"source":0,"target":18,"value":8},{"source":0,"target":19,"value":10},{"source":0,"target":20,"value":6},
         {"source":0,"target":21,"value":2},{"source":0,"target":22,"value":8},{"source":0,"target":23,"value":10},{"source":0,"target":24,"value":6},
         {"source":0,"target":25,"value":2},{"source":0,"target":26,"value":8},{"source":0,"target":27,"value":10},{"source":0,"target":28,"value":6},
         {"source":0,"target":29,"value":2},{"source":0,"target":30,"value":8},{"source":0,"target":31,"value":10},
         {"source":1,"target":0,"value":1},{"source":2,"target":0,"value":8},{"source":3,"target":0,"value":10},{"source":3,"target":2,"value":6},
         {"source":4,"target":0,"value":1},{"source":5,"target":0,"value":1},{"source":6,"target":0,"value":1},{"source":7,"target":0,"value":1},
         {"source":8,"target":0,"value":2},{"source":9,"target":0,"value":1},{"source":11,"target":10,"value":1},{"source":11,"target":3,"value":3},
         {"source":11,"target":2,"value":3},{"source":11,"target":0,"value":5},{"source":12,"target":11,"value":1},{"source":13,"target":11,"value":1},
         {"source":14,"target":11,"value":1},{"source":15,"target":11,"value":1},{"source":17,"target":16,"value":4},{"source":18,"target":16,"value":4},
         {"source":18,"target":17,"value":4},{"source":19,"target":16,"value":4},{"source":19,"target":17,"value":4},{"source":19,"target":18,"value":4},
         {"source":20,"target":16,"value":3},{"source":20,"target":17,"value":3},{"source":20,"target":18,"value":3},{"source":20,"target":19,"value":4},
         {"source":21,"target":16,"value":3},{"source":21,"target":17,"value":3},{"source":21,"target":18,"value":3},{"source":21,"target":19,"value":3},
         {"source":21,"target":20,"value":5},{"source":22,"target":16,"value":3},{"source":22,"target":17,"value":3},{"source":22,"target":18,"value":3},
         {"source":22,"target":19,"value":3},{"source":22,"target":20,"value":4},{"source":22,"target":21,"value":4},{"source":23,"target":16,"value":3},
         {"source":23,"target":17,"value":3},{"source":23,"target":18,"value":3},{"source":23,"target":19,"value":3},{"source":23,"target":20,"value":4},
         {"source":23,"target":21,"value":4},{"source":23,"target":22,"value":4},{"source":23,"target":12,"value":2},{"source":23,"target":11,"value":9},
         {"source":24,"target":23,"value":2},{"source":24,"target":11,"value":7},{"source":25,"target":24,"value":13},{"source":25,"target":23,"value":1},
         {"source":25,"target":11,"value":12},{"source":26,"target":24,"value":4},{"source":26,"target":11,"value":31},{"source":26,"target":16,"value":1},
         {"source":26,"target":25,"value":1},{"source":27,"target":11,"value":17},{"source":27,"target":23,"value":5},{"source":27,"target":25,"value":5},
         {"source":27,"target":24,"value":1},{"source":27,"target":26,"value":1},{"source":28,"target":11,"value":8},{"source":28,"target":27,"value":1},
         {"source":29,"target":23,"value":1},{"source":29,"target":27,"value":1},{"source":29,"target":11,"value":2},{"source":30,"target":23,"value":1},
         {"source":31,"target":30,"value":2}]}

hashtags_result = {"nodes":[{"text":"#OpenData","type":"tag","id":"2","r":5,"fixed":True,"angle":0},
                            {"text":"#avoindata","type":"tag","id":"1383","r":5,"fixed":True,"angle":0.48332194670612},
                            {"text":"#okfn","type":"tag","id":"24","r":5,"fixed":True,"angle":0.96664389341224},
                            {"text":"#opengov","type":"tag","id":"42","r":5,"fixed":True,"angle":1.4499658401184},
                            {"text":"#job","type":"tag","id":"2560","r":5,"fixed":True,"angle":1.9332877868245},
                            {"text":"#OKF","type":"tag","id":"1618","r":5,"fixed":True,"angle":2.4166097335306},
                            {"text":"#opensustainability","type":"tag","id":"2129","r":5,"fixed":True,"angle":2.8999316802367},
                            {"text":"#OpenParl","type":"tag","id":"1457","r":5,"fixed":True,"angle":3.3832536269429},
                            {"text":"#transparency","type":"tag","id":"1394","r":5,"fixed":True,"angle":3.866575573649},
                            {"text":"#Meemoo","type":"tag","id":"1787","r":5,"fixed":True,"angle":4.3498975203551},
                            {"text":"#opendev","type":"tag","id":"41","r":5,"fixed":True,"angle":4.8332194670612},
                            {"text":"#ogp","type":"tag","id":"1451","r":5,"fixed":True,"angle":5.3165414137673},
                            {"text":"#bigcleancz","type":"tag","id":"2556","r":5,"fixed":True,"angle":5.7998633604735},
                            {"id":"291320874487906306",
                             "text":"#opendev #okfest. Why #internet freedom is important for #development #aaron #swartz http:\/\/t.co\/1Tljpp70",
                             "user":"davidglobal","type":"linked","r":5},
                            {"id":"290872942022250497",
                             "text":"OKfestival 2012 | Helsinki Finland http:\/\/t.co\/zXPa0tIu #okfest #opendata",
                             "user":"up_tanja","type":"linked","r":5},{"id":"288726224031846400","text":"Having a phone meeting with @markcardwell, @ruthdelcampo &amp; Jake Garcia - a few great #OpenDev ppl in NYC I also met at #OKFest! Hello again!","user":"pernillan","type":"linked","r":5},{"id":"287649838940704768","text":"RT @meowtree: Help! What data set did US public download most when USG open its data? goats? donkeys? #opendata #opengov? #okfest","user":"GovernmentBot","type":"linked","r":5},{"id":"287623518978457600","text":"@socrata know this? RT @meowtree: Help! What data set did US public download most when USG open its data? #opendata #opengov? #okfest","user":"greerjacob","type":"linked","r":5},{"id":"287621297364668417","text":"Help! What data set did US public download most when USG open its data? goats? donkeys? #opendata #opengov? #okfest","user":"meowtree","type":"linked","r":5},{"id":"287552820863971328","text":"Help! What was data set that US public was interested in\/downloaded most when USG began doing #opendata #opengov? #okfest @tkb @freebalance","user":"meowtree","type":"linked","r":5},{"id":"281125129503793152","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"arongas","type":"linked","r":5},{"id":"281101061853421568","text":"RT @JoonasD6: Going to #OKFN Finland founding meeting this Friday http:\/\/t.co\/9rfzsQRI #avoindata #OKfest #opendata RY, not a foundation, though. :)","user":"italiaopendata","type":"linked","r":5},{"id":"281098700695158784","text":"RT @JoonasD6: Going to #OKFN Finland founding meeting this Friday http:\/\/t.co\/9rfzsQRI #avoindata #OKfest #opendata RY, not a foundation, though. :)","user":"OpenDataIT","type":"linked","r":5},{"id":"281098547141697536","text":"Going to #OKFN Finland founding meeting this Friday http:\/\/t.co\/9rfzsQRI #avoindata #OKfest #opendata RY, not a foundation, though. :)","user":"JoonasD6","type":"linked","r":5},{"id":"280978795417174017","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"miskaknapek","type":"linked","r":5},{"id":"280952387684929536","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"jusnis","type":"linked","r":5},{"id":"280947895459528704","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"ReettaTuulia","type":"linked","r":5},{"id":"280928899918073856","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"pe3","type":"linked","r":5},{"id":"280924819330064384","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"188000Lakes","type":"linked","r":5},{"id":"280923109916282881","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"jarmolahti","type":"linked","r":5},{"id":"280921343506149376","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"ouzor","type":"linked","r":5},{"id":"280821358118711296","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"OpenDataIT","type":"linked","r":5},{"id":"280811113086586881","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"italiaopendata","type":"linked","r":5},{"id":"280806930157551616","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 1PM http:\/\/t.co\/huo2HVMK #avoindata #OKfest #opendata","user":"Datajournalismi","type":"linked","r":5},{"id":"280806811832029185","text":"RT @apoikola: Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 1PM http:\/\/t.co\/2jq8a8q2 #avoindata #OKfest #opendata","user":"OKFestival","type":"linked","r":5},{"id":"280806492414808065","text":"Founding meeting of the #okfn Finland association (ry.) Fri 21.12.2012 at 1 PM http:\/\/t.co\/yYS3OEKT #avoindata #OKfest #opendata","user":"apoikola","type":"linked","r":5},{"id":"278159327238434816","text":"With @fininstlondon, we're publishing The Open Book re: #opendata and #openknowledge - and we want your help! http:\/\/t.co\/GasMadDV #okfest","user":"kat_braybrooke","type":"linked","r":5},{"id":"276353306861907968","text":"RT @vndimitrova: Launching the Open Sustainability Working Group http:\/\/t.co\/jhF6SMAo #opendata #opensustainability #okfest @zapico","user":"OpenDataIT","type":"linked","r":5},{"id":"276349961380179969","text":"RT @vndimitrova: Launching the Open Sustainability Working Group http:\/\/t.co\/jhF6SMAo #opendata #opensustainability #okfest @zapico","user":"arthurvdmolen","type":"linked","r":5},{"id":"274862849241776128","text":"Transport Data Workshop Proceedings | European Public Sector Information Platform | @scoopit http:\/\/t.co\/LPHO0SZj #OpenData #OKFest","user":"iradche","type":"linked","r":5},{"id":"274601406772678657","text":"RT @okfnecon: Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"fontanon","type":"linked","r":5},{"id":"274587904204996608","text":"Just signed up! RT @vndimitrova: Launching the Open Sustainability Working Group http:\/\/t.co\/uRnFsimh #opendata #opensustainability #okfest","user":"adstiles","type":"linked","r":5},{"id":"274573180402806785","text":"RT @vndimitrova: Launching the Open Sustainability Working Group http:\/\/t.co\/jhF6SMAo #opendata #opensustainability #okfest @zapico","user":"okfngr","type":"linked","r":5},{"id":"274570771932786689","text":"RT @vndimitrova: Launching the Open Sustainability Working Group http:\/\/t.co\/jhF6SMAo #opendata #opensustainability #okfest @zapico","user":"ChrisMartin81","type":"linked","r":5},{"id":"274561466672218112","text":"RT @okfnecon: Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"arthurvdmolen","type":"linked","r":5},{"id":"274538388206522368","text":"RT @okfnecon: Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"OpenDataIT","type":"linked","r":5},{"id":"274535842322731008","text":"RT @okfnecon: Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"ehoorn","type":"linked","r":5},{"id":"274523707253342209","text":"RT @okfnecon: Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"zapico","type":"linked","r":5},{"id":"274518116950740993","text":"RT @okfnecon: Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"electricbum","type":"linked","r":5},{"id":"274516874442706945","text":"RT @okfnecon: Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"Floppy","type":"linked","r":5},{"id":"274516621484236800","text":"RT @okfnecon: Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"JackTownsend_","type":"linked","r":5},{"id":"274516222287171584","text":"Launching Open Sustainability http:\/\/t.co\/gt9TMPT5 #opendata #okfest @zapico @JackTownsend_ @electricbum @Floppy @mrchrisadams @vndimitrova","user":"okfnecon","type":"linked","r":5},{"id":"274515911132721152","text":"Launching the Open Sustainability Working Group http:\/\/t.co\/jhF6SMAo #opendata #opensustainability #okfest @zapico","user":"vndimitrova","type":"linked","r":5},{"id":"274068122078699520","text":"Transport Data Workshop Proceedings | European Public Sector Information Platform | @scoopit http:\/\/t.co\/LPHO0SZj #OpenData #OKFest","user":"iradche","type":"linked","r":5},{"id":"273419013479079937","text":"RT @apoikola: #okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/ds3tBZd8 #avoindata #okfest #opendata","user":"HSLdevcom","type":"linked","r":5},{"id":"273412713596743680","text":"RT @apoikola: #okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/ds3tBZd8 #avoindata #okfest #opendata","user":"jusnis","type":"linked","r":5},{"id":"273407497933582337","text":"RT @apoikola: #okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/ds3tBZd8 #avoindata #okfest #opendata","user":"okfngr","type":"linked","r":5},{"id":"273395715428974594","text":"RT @ra__mu: RT @apoikola: #okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/CgFe6zFc  #okfest #opendata","user":"tatitosi","type":"linked","r":5},{"id":"273391429240385536","text":"RT @apoikola: #okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/ds3tBZd8 #avoindata #okfest #opendata","user":"ra__mu","type":"linked","r":5},{"id":"273389922302451713","text":"RT @apoikola: #okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/ds3tBZd8 #avoindata #okfest #opendata","user":"OpenDataIT","type":"linked","r":5},{"id":"273386682433286146","text":"RT @apoikola: #okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/ds3tBZd8 #avoindata #okfest #opendata","user":"ajhalo","type":"linked","r":5},{"id":"273372198931152896","text":"RT @apoikola: #okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/ds3tBZd8 #avoindata #okfest #opendata","user":"miclovich","type":"linked","r":5},{"id":"273370419023712256","text":"RT @apoikola: #okfn-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/frQ0T2sv #avoindata #okfest #opendata","user":"OKFestival","type":"linked","r":5},{"id":"273370087543697409","text":"#okf-finland convention 8-9 Feb 2013: Call for Proposals is open now! http:\/\/t.co\/ds3tBZd8 #avoindata #okfest #opendata","user":"apoikola","type":"linked","r":5},{"id":"271982285673332739","text":"RT @alanhudson1: #OKFest 2012 One Month Later: Successes and Happy Tidings (via @OKFN) #opengov http:\/\/t.co\/ksvfMKFG #opendata","user":"OpenDataIT","type":"linked","r":5},{"id":"271976602190098432","text":"RT @alanhudson1: #OKFest 2012 One Month Later: Successes and Happy Tidings (via @OKFN) #opengov http:\/\/t.co\/ksvfMKFG #opendata","user":"GovernmentBot","type":"linked","r":5},{"id":"271957510125154305","text":"#OKFest 2012 One Month Later: Successes and Happy Tidings (via @OKFN) #opengov http:\/\/t.co\/ksvfMKFG #opendata","user":"alanhudson1","type":"linked","r":5},{"id":"268603033515077632","text":"#okfest MT @hansrosling: Sanjay Pradhan mapping #opendata on detailed community level 2 make tax &amp; aid end poverty http:\/\/t.co\/DehlyPME #TED","user":"merelyanode","type":"linked","r":5},{"id":"268410431935221760","text":"Parminder's Q &amp; @ethanZ's response reminds me of #okfest #opendev discussion of need for structure and rules to make openness work #openup12","user":"timdavies","type":"linked","r":5},{"id":"268298559001096192","text":"@mshouji Congrats from Finland!  Last time I was in Japan was in 1997! Gambate ne! :) #avoindata #okfn #okfest","user":"mshelsinki","type":"linked","r":5},{"id":"268281842053050368","text":"Checking out possible venue for the OKF Finland convention 8-9.2.2013 #avoindata #okfn #okfest (@ Tuusulan Onnela) http:\/\/t.co\/YOWA9rfV","user":"apoikola","type":"linked","r":5},{"id":"268157128949243905","text":"#OKFN Japan group @okfj hold its launch party today!  We welcome your congratulations messages, pictures, and videos! #okfest #opendata","user":"mshouji","type":"linked","r":5},{"id":"268000233416425472","text":"RT @Jacattell: Hello @Newmanlk. Found #OKFest http:\/\/t.co\/ceiRN3Le and could add http:\/\/t.co\/S5msgnFA. #opendata","user":"tatitosi","type":"linked","r":5},{"id":"266913636377833472","text":"iPhone notes flashback: @pthigo at #okfest \"if someone has lived in poverty for 25-30 years, they are the experts in poverty\" #opendev","user":"KimBorrowdale","type":"linked","r":5},{"id":"266828247784882176","text":"Hello @Newmanlk. Found #OKFest http:\/\/t.co\/HYn4ZEkM and could add http:\/\/t.co\/S18Xvv7O. Are you collaborating online, please? #opendata","user":"Jacattell","type":"linked","r":5},{"id":"266827495276412928","text":"@geocomputer @snim2 @volcanodance @rastrau @puntofisso and if that link doesn't work, try http:\/\/t.co\/HYn4ZEkM #OKFest #OpenData #research","user":"Jacattell","type":"linked","r":5},{"id":"266827062050963456","text":"@geocomputer @snim2 @volcanodance Re http:\/\/t.co\/S18Xvv7O, see #OKFest #OpenData Academic Research http:\/\/t.co\/eOWofQyF @rastrau @puntofisso","user":"Jacattell","type":"linked","r":5},{"id":"266601483989053440","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"markheseltine","type":"linked","r":5},{"id":"266488402881433600","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"l_dickey","type":"linked","r":5},{"id":"266484210011893760","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"openp2pdesign","type":"linked","r":5},{"id":"266482308960358400","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"OKFestival","type":"linked","r":5},{"id":"266481971071430656","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"thekarin","type":"linked","r":5},{"id":"266480824843644928","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"eldelacajita","type":"linked","r":5},{"id":"266480709605146624","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"Info_Activism","type":"linked","r":5},{"id":"266479724602200064","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"piezanowski","type":"linked","r":5},{"id":"266479597644836864","text":"RT @kat_braybrooke: Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"houndbee","type":"linked","r":5},{"id":"266479320078364673","text":"Big news for those into #OKFest 2012 - the @OKFN is hiring an Events Coordinator to help organise the 2013 event: http:\/\/t.co\/0NWHf6RX #job","user":"kat_braybrooke","type":"linked","r":5},{"id":"265152592336797698","text":"RT @BigCleanCZ: Pre-#bigcleancz at @DOXPrague: Juha Huuskonen reflecting on #okfest. http:\/\/t.co\/yLeLDpMW","user":"miskaknapek","type":"linked","r":5},{"id":"264797011373588480","text":"RT @forresto: Here is my #meemoo HTML5 video looper from #okfest :-) about: http:\/\/t.co\/w6AJGxTW live: http:\/\/t.co\/BXTEyKXg pic: http:\/\/t.co\/6IXmBw4I","user":"ARTEKLAB","type":"linked","r":5},{"id":"264417329553739776","text":"RT @BigCleanCZ: Pre-#bigcleancz at @DOXPrague: Juha Huuskonen reflecting on #okfest. http:\/\/t.co\/yLeLDpMW","user":"DOXPrague","type":"linked","r":5},{"id":"264414489682780160","text":"Pre-#bigcleancz at @DOXPrague: Juha Huuskonen reflecting on #okfest. http:\/\/t.co\/yLeLDpMW","user":"BigCleanCZ","type":"linked","r":5},{"id":"264392270189576193","text":"RT @forresto: Here is my #meemoo HTML5 video looper from #okfest :-) about: http:\/\/t.co\/w6AJGxTW live: http:\/\/t.co\/BXTEyKXg pic: http:\/\/t.co\/6IXmBw4I","user":"OpenGLAM","type":"linked","r":5},{"id":"264205745057316864","text":"The new default is: if you're going to cite the data , you might as well link to it. (Weinberger 2011) #opendata #openscience #okfest","user":"niitamo","type":"linked","r":5},{"id":"264161887560806400","text":"RT @forresto: Here is my #meemoo HTML5 video looper from #okfest :-) about: http:\/\/t.co\/w6AJGxTW live: http:\/\/t.co\/BXTEyKXg pic: http:\/\/t.co\/6IXmBw4I","user":"OKFestival","type":"linked","r":5},{"id":"264161789904826368","text":"RT @alanhudson1: Great #OKFest talk on @participatory budgeting + leveraging dispersed knowledge by Tiago Peixoto http:\/\/t.co\/0Luc3WaH #opendata #OGP @OKFN","user":"kat_braybrooke","type":"linked","r":5},{"id":"264161792211705856","text":"RT @alanhudson1: Great #OKFest talk on @participatory budgeting + leveraging dispersed knowledge by Tiago Peixoto http:\/\/t.co\/0Luc3WaH #opendata #OGP @OKFN","user":"OKFestival","type":"linked","r":5},{"id":"264128967987040257","text":"Great #OKFest talk on @participatory budgeting + leveraging dispersed knowledge by Tiago Peixoto http:\/\/t.co\/0Luc3WaH #opendata #OGP @OKFN","user":"alanhudson1","type":"linked","r":5},{"id":"264108398314942465","text":"Here is my #meemoo HTML5 video looper from #okfest :-) about: http:\/\/t.co\/w6AJGxTW live: http:\/\/t.co\/BXTEyKXg pic: http:\/\/t.co\/6IXmBw4I","user":"forresto","type":"linked","r":5},{"id":"263602354497126400","text":"RT @RegardsCitoyens: All videos from #OKFest talks on #OpenParl #OpenData #OpenGov &amp; #Transparency gathered here http:\/\/t.co\/hA8lT3ny &amp; here http:\/\/t.co\/YH3JUGvc","user":"piezanowski","type":"linked","r":5},{"id":"263022059435728896","text":"OKFestival 2012 One Month Later: Successes and Happy Tidings ... http:\/\/t.co\/RjYhLSFf #okfest #opendata #lodlam (via @kat_braybrooke)","user":"hashonomy_gus","type":"linked","r":5},{"id":"262908554057486337","text":"RT @RegardsCitoyens: All videos from #OKFest talks on #OpenParl #OpenData #OpenGov &amp; #Transparency gathered here http:\/\/t.co\/hA8lT3ny &amp; here http:\/\/t.co\/YH3JUGvc","user":"agm3dc","type":"linked","r":5},{"id":"262906913505828864","text":"RT @RegardsCitoyens: All videos from #OKFest talks on #OpenParl #OpenData #OpenGov &amp; #Transparency gathered here http:\/\/t.co\/hA8lT3ny &amp; here http:\/\/t.co\/YH3JUGvc","user":"LiberTIC","type":"linked","r":5},{"id":"262905949231132672","text":"RT @RegardsCitoyens: All videos from #OKFest talks on #OpenParl #OpenData #OpenGov &amp; #Transparency gathered here http:\/\/t.co\/hA8lT3ny &amp; here http:\/\/t.co\/YH3JUGvc","user":"ferdinandboas","type":"linked","r":5},{"id":"262905647044104192","text":"All videos from #OKFest talks on #OpenParl #OpenData #OpenGov &amp; #Transparency gathered here http:\/\/t.co\/hA8lT3ny &amp; here http:\/\/t.co\/YH3JUGvc","user":"RegardsCitoyens","type":"linked","r":5},{"id":"262905593055019008","text":"Un mois apr\u00e8s:le bilan chiffr\u00e9 &amp; vid\u00e9o de l'#OKFest \u00e0 #Helsinki by @OKFN http:\/\/t.co\/53oNY0V4 RDV l'an prochain \u00e0 Gen\u00e8ve! #OpenData #OpenGov","user":"RegardsCitoyens","type":"linked","r":5},{"id":"262902428742062080","text":"Post by @OKFN about #OKFest 2012 and sneak preview for 2013: http:\/\/t.co\/PakUJiZd #opendata #lodlam #GLAM via @OKFestival","user":"maxkaiser","type":"linked","r":5},{"id":"262508122629894144","text":"RT @davenportsteve: The Open Data Effect: Creating Optimistic Radicals at OKFest http:\/\/t.co\/Vnfj1ZEC #OKFest #opendata","user":"alanhudson1","type":"linked","r":5},{"id":"261075460925050880","text":"RT @BigCleanCZ: On the eve of #bigcleancz, @juhuutweet will talk at @DOXPrague about #okfest, art and politics. http:\/\/t.co\/MtldyDpr http:\/\/t.co\/TjeJ9Zfr","user":"PLUSChrisM","type":"linked","r":5},{"id":"261067198032928768","text":"RT @BigCleanCZ: On the eve of #bigcleancz, @juhuutweet will talk at @DOXPrague about #okfest, art and politics. http:\/\/t.co\/MtldyDpr http:\/\/t.co\/TjeJ9Zfr","user":"DOXPrague","type":"linked","r":5},{"id":"261060984322535424","text":"RT @BigCleanCZ: On the eve of #bigcleancz, @juhuutweet will talk at @DOXPrague about #okfest, art and politics. http:\/\/t.co\/MtldyDpr http:\/\/t.co\/TjeJ9Zfr","user":"jindrichmynarz","type":"linked","r":5},{"id":"261060871260880896","text":"On the eve of #bigcleancz, @juhuutweet will talk at @DOXPrague about #okfest, art and politics. http:\/\/t.co\/MtldyDpr http:\/\/t.co\/TjeJ9Zfr","user":"BigCleanCZ","type":"linked","r":5},{"id":"261005483563970560","text":"#opengov partnership in FI draft roadmap http:\/\/t.co\/3aZNNPjp  #Citizen #Participation is key focus  #OKFest 2012","user":"openlivinglabs","type":"linked","r":5},{"id":"260821661954228225","text":"Todos los v\u00eddeos del #OKFest de @OKFN en http:\/\/t.co\/UGfmi3kA  #oGov #opendata: Todos los v\u00eddeos del #OKFest de ... http:\/\/t.co\/VgxNDkhi","user":"_opendata","type":"linked","r":5}],"links":[{"id":"41->291320874487906306","targetid":"291320874487906306","sourceid":"41"},{"id":"2->290872942022250497","targetid":"290872942022250497","sourceid":"2"},{"id":"41->288726224031846400","targetid":"288726224031846400","sourceid":"41"},{"id":"2->287649838940704768","targetid":"287649838940704768","sourceid":"2"},{"id":"42->287649838940704768","targetid":"287649838940704768","sourceid":"42"},{"id":"2->287623518978457600","targetid":"287623518978457600","sourceid":"2"},{"id":"42->287623518978457600","targetid":"287623518978457600","sourceid":"42"},{"id":"2->287621297364668417","targetid":"287621297364668417","sourceid":"2"},{"id":"42->287621297364668417","targetid":"287621297364668417","sourceid":"42"},{"id":"2->287552820863971328","targetid":"287552820863971328","sourceid":"2"},{"id":"42->287552820863971328","targetid":"287552820863971328","sourceid":"42"},{"id":"24->281125129503793152","targetid":"281125129503793152","sourceid":"24"},{"id":"1383->281125129503793152","targetid":"281125129503793152","sourceid":"1383"},{"id":"2->281125129503793152","targetid":"281125129503793152","sourceid":"2"},{"id":"24->281101061853421568","targetid":"281101061853421568","sourceid":"24"},{"id":"1383->281101061853421568","targetid":"281101061853421568","sourceid":"1383"},{"id":"2->281101061853421568","targetid":"281101061853421568","sourceid":"2"},{"id":"24->281098700695158784","targetid":"281098700695158784","sourceid":"24"},{"id":"1383->281098700695158784","targetid":"281098700695158784","sourceid":"1383"},{"id":"2->281098700695158784","targetid":"281098700695158784","sourceid":"2"},{"id":"24->281098547141697536","targetid":"281098547141697536","sourceid":"24"},{"id":"1383->281098547141697536","targetid":"281098547141697536","sourceid":"1383"},{"id":"2->281098547141697536","targetid":"281098547141697536","sourceid":"2"},{"id":"24->280978795417174017","targetid":"280978795417174017","sourceid":"24"},{"id":"1383->280978795417174017","targetid":"280978795417174017","sourceid":"1383"},{"id":"2->280978795417174017","targetid":"280978795417174017","sourceid":"2"},{"id":"24->280952387684929536","targetid":"280952387684929536","sourceid":"24"},{"id":"1383->280952387684929536","targetid":"280952387684929536","sourceid":"1383"},{"id":"2->280952387684929536","targetid":"280952387684929536","sourceid":"2"},{"id":"24->280947895459528704","targetid":"280947895459528704","sourceid":"24"},{"id":"1383->280947895459528704","targetid":"280947895459528704","sourceid":"1383"},{"id":"2->280947895459528704","targetid":"280947895459528704","sourceid":"2"},{"id":"24->280928899918073856","targetid":"280928899918073856","sourceid":"24"},{"id":"1383->280928899918073856","targetid":"280928899918073856","sourceid":"1383"},{"id":"2->280928899918073856","targetid":"280928899918073856","sourceid":"2"},{"id":"24->280924819330064384","targetid":"280924819330064384","sourceid":"24"},{"id":"1383->280924819330064384","targetid":"280924819330064384","sourceid":"1383"},{"id":"2->280924819330064384","targetid":"280924819330064384","sourceid":"2"},{"id":"24->280923109916282881","targetid":"280923109916282881","sourceid":"24"},{"id":"1383->280923109916282881","targetid":"280923109916282881","sourceid":"1383"},{"id":"2->280923109916282881","targetid":"280923109916282881","sourceid":"2"},{"id":"24->280921343506149376","targetid":"280921343506149376","sourceid":"24"},{"id":"1383->280921343506149376","targetid":"280921343506149376","sourceid":"1383"},{"id":"2->280921343506149376","targetid":"280921343506149376","sourceid":"2"},{"id":"24->280821358118711296","targetid":"280821358118711296","sourceid":"24"},{"id":"1383->280821358118711296","targetid":"280821358118711296","sourceid":"1383"},{"id":"2->280821358118711296","targetid":"280821358118711296","sourceid":"2"},{"id":"24->280811113086586881","targetid":"280811113086586881","sourceid":"24"},{"id":"1383->280811113086586881","targetid":"280811113086586881","sourceid":"1383"},{"id":"2->280811113086586881","targetid":"280811113086586881","sourceid":"2"},{"id":"24->280806930157551616","targetid":"280806930157551616","sourceid":"24"},{"id":"1383->280806930157551616","targetid":"280806930157551616","sourceid":"1383"},{"id":"2->280806930157551616","targetid":"280806930157551616","sourceid":"2"},{"id":"24->280806811832029185","targetid":"280806811832029185","sourceid":"24"},{"id":"1383->280806811832029185","targetid":"280806811832029185","sourceid":"1383"},{"id":"2->280806811832029185","targetid":"280806811832029185","sourceid":"2"},{"id":"24->280806492414808065","targetid":"280806492414808065","sourceid":"24"},{"id":"1383->280806492414808065","targetid":"280806492414808065","sourceid":"1383"},{"id":"2->280806492414808065","targetid":"280806492414808065","sourceid":"2"},{"id":"2->278159327238434816","targetid":"278159327238434816","sourceid":"2"},{"id":"2->276353306861907968","targetid":"276353306861907968","sourceid":"2"},{"id":"2129->276353306861907968","targetid":"276353306861907968","sourceid":"2129"},{"id":"2->276349961380179969","targetid":"276349961380179969","sourceid":"2"},{"id":"2129->276349961380179969","targetid":"276349961380179969","sourceid":"2129"},{"id":"2->274862849241776128","targetid":"274862849241776128","sourceid":"2"},{"id":"2->274601406772678657","targetid":"274601406772678657","sourceid":"2"},{"id":"2->274587904204996608","targetid":"274587904204996608","sourceid":"2"},{"id":"2129->274587904204996608","targetid":"274587904204996608","sourceid":"2129"},{"id":"2->274573180402806785","targetid":"274573180402806785","sourceid":"2"},{"id":"2129->274573180402806785","targetid":"274573180402806785","sourceid":"2129"},{"id":"2->274570771932786689","targetid":"274570771932786689","sourceid":"2"},{"id":"2129->274570771932786689","targetid":"274570771932786689","sourceid":"2129"},{"id":"2->274561466672218112","targetid":"274561466672218112","sourceid":"2"},{"id":"2->274538388206522368","targetid":"274538388206522368","sourceid":"2"},{"id":"2->274535842322731008","targetid":"274535842322731008","sourceid":"2"},{"id":"2->274523707253342209","targetid":"274523707253342209","sourceid":"2"},{"id":"2->274518116950740993","targetid":"274518116950740993","sourceid":"2"},{"id":"2->274516874442706945","targetid":"274516874442706945","sourceid":"2"},{"id":"2->274516621484236800","targetid":"274516621484236800","sourceid":"2"},{"id":"2->274516222287171584","targetid":"274516222287171584","sourceid":"2"},{"id":"2->274515911132721152","targetid":"274515911132721152","sourceid":"2"},{"id":"2129->274515911132721152","targetid":"274515911132721152","sourceid":"2129"},{"id":"2->274068122078699520","targetid":"274068122078699520","sourceid":"2"},{"id":"1618->273419013479079937","targetid":"273419013479079937","sourceid":"1618"},{"id":"1383->273419013479079937","targetid":"273419013479079937","sourceid":"1383"},{"id":"2->273419013479079937","targetid":"273419013479079937","sourceid":"2"},{"id":"1618->273412713596743680","targetid":"273412713596743680","sourceid":"1618"},{"id":"1383->273412713596743680","targetid":"273412713596743680","sourceid":"1383"},{"id":"2->273412713596743680","targetid":"273412713596743680","sourceid":"2"},{"id":"1618->273407497933582337","targetid":"273407497933582337","sourceid":"1618"},{"id":"1383->273407497933582337","targetid":"273407497933582337","sourceid":"1383"},{"id":"2->273407497933582337","targetid":"273407497933582337","sourceid":"2"},{"id":"1618->273395715428974594","targetid":"273395715428974594","sourceid":"1618"},{"id":"2->273395715428974594","targetid":"273395715428974594","sourceid":"2"},{"id":"1618->273391429240385536","targetid":"273391429240385536","sourceid":"1618"},{"id":"1383->273391429240385536","targetid":"273391429240385536","sourceid":"1383"},{"id":"2->273391429240385536","targetid":"273391429240385536","sourceid":"2"},{"id":"1618->273389922302451713","targetid":"273389922302451713","sourceid":"1618"},{"id":"1383->273389922302451713","targetid":"273389922302451713","sourceid":"1383"},{"id":"2->273389922302451713","targetid":"273389922302451713","sourceid":"2"},{"id":"1618->273386682433286146","targetid":"273386682433286146","sourceid":"1618"},{"id":"1383->273386682433286146","targetid":"273386682433286146","sourceid":"1383"},{"id":"2->273386682433286146","targetid":"273386682433286146","sourceid":"2"},{"id":"1618->273372198931152896","targetid":"273372198931152896","sourceid":"1618"},{"id":"1383->273372198931152896","targetid":"273372198931152896","sourceid":"1383"},{"id":"2->273372198931152896","targetid":"273372198931152896","sourceid":"2"},{"id":"24->273370419023712256","targetid":"273370419023712256","sourceid":"24"},{"id":"1383->273370419023712256","targetid":"273370419023712256","sourceid":"1383"},{"id":"2->273370419023712256","targetid":"273370419023712256","sourceid":"2"},{"id":"1618->273370087543697409","targetid":"273370087543697409","sourceid":"1618"},{"id":"1383->273370087543697409","targetid":"273370087543697409","sourceid":"1383"},{"id":"2->273370087543697409","targetid":"273370087543697409","sourceid":"2"},{"id":"42->271982285673332739","targetid":"271982285673332739","sourceid":"42"},{"id":"2->271982285673332739","targetid":"271982285673332739","sourceid":"2"},{"id":"42->271976602190098432","targetid":"271976602190098432","sourceid":"42"},{"id":"2->271976602190098432","targetid":"271976602190098432","sourceid":"2"},{"id":"42->271957510125154305","targetid":"271957510125154305","sourceid":"42"},{"id":"2->271957510125154305","targetid":"271957510125154305","sourceid":"2"},{"id":"2->268603033515077632","targetid":"268603033515077632","sourceid":"2"},{"id":"41->268410431935221760","targetid":"268410431935221760","sourceid":"41"},{"id":"1383->268298559001096192","targetid":"268298559001096192","sourceid":"1383"},{"id":"24->268298559001096192","targetid":"268298559001096192","sourceid":"24"},{"id":"1383->268281842053050368","targetid":"268281842053050368","sourceid":"1383"},{"id":"24->268281842053050368","targetid":"268281842053050368","sourceid":"24"},{"id":"24->268157128949243905","targetid":"268157128949243905","sourceid":"24"},{"id":"2->268157128949243905","targetid":"268157128949243905","sourceid":"2"},{"id":"2->268000233416425472","targetid":"268000233416425472","sourceid":"2"},{"id":"41->266913636377833472","targetid":"266913636377833472","sourceid":"41"},{"id":"2->266828247784882176","targetid":"266828247784882176","sourceid":"2"},{"id":"2->266827495276412928","targetid":"266827495276412928","sourceid":"2"},{"id":"2->266827062050963456","targetid":"266827062050963456","sourceid":"2"},{"id":"2560->266601483989053440","targetid":"266601483989053440","sourceid":"2560"},{"id":"2560->266488402881433600","targetid":"266488402881433600","sourceid":"2560"},{"id":"2560->266484210011893760","targetid":"266484210011893760","sourceid":"2560"},{"id":"2560->266482308960358400","targetid":"266482308960358400","sourceid":"2560"},{"id":"2560->266481971071430656","targetid":"266481971071430656","sourceid":"2560"},{"id":"2560->266480824843644928","targetid":"266480824843644928","sourceid":"2560"},{"id":"2560->266480709605146624","targetid":"266480709605146624","sourceid":"2560"},{"id":"2560->266479724602200064","targetid":"266479724602200064","sourceid":"2560"},{"id":"2560->266479597644836864","targetid":"266479597644836864","sourceid":"2560"},{"id":"2560->266479320078364673","targetid":"266479320078364673","sourceid":"2560"},{"id":"2556->265152592336797698","targetid":"265152592336797698","sourceid":"2556"},{"id":"1787->264797011373588480","targetid":"264797011373588480","sourceid":"1787"},{"id":"2556->264417329553739776","targetid":"264417329553739776","sourceid":"2556"},{"id":"2556->264414489682780160","targetid":"264414489682780160","sourceid":"2556"},{"id":"1787->264392270189576193","targetid":"264392270189576193","sourceid":"1787"},{"id":"2->264205745057316864","targetid":"264205745057316864","sourceid":"2"},{"id":"1787->264161887560806400","targetid":"264161887560806400","sourceid":"1787"},{"id":"2->264161789904826368","targetid":"264161789904826368","sourceid":"2"},{"id":"1451->264161789904826368","targetid":"264161789904826368","sourceid":"1451"},{"id":"2->264161792211705856","targetid":"264161792211705856","sourceid":"2"},{"id":"1451->264161792211705856","targetid":"264161792211705856","sourceid":"1451"},{"id":"2->264128967987040257","targetid":"264128967987040257","sourceid":"2"},{"id":"1451->264128967987040257","targetid":"264128967987040257","sourceid":"1451"},{"id":"1787->264108398314942465","targetid":"264108398314942465","sourceid":"1787"},{"id":"1457->263602354497126400","targetid":"263602354497126400","sourceid":"1457"},{"id":"2->263602354497126400","targetid":"263602354497126400","sourceid":"2"},{"id":"42->263602354497126400","targetid":"263602354497126400","sourceid":"42"},{"id":"1394->263602354497126400","targetid":"263602354497126400","sourceid":"1394"},{"id":"2->263022059435728896","targetid":"263022059435728896","sourceid":"2"},{"id":"1457->262908554057486337","targetid":"262908554057486337","sourceid":"1457"},{"id":"2->262908554057486337","targetid":"262908554057486337","sourceid":"2"},{"id":"42->262908554057486337","targetid":"262908554057486337","sourceid":"42"},{"id":"1394->262908554057486337","targetid":"262908554057486337","sourceid":"1394"},{"id":"1457->262906913505828864","targetid":"262906913505828864","sourceid":"1457"},{"id":"2->262906913505828864","targetid":"262906913505828864","sourceid":"2"},{"id":"42->262906913505828864","targetid":"262906913505828864","sourceid":"42"},{"id":"1394->262906913505828864","targetid":"262906913505828864","sourceid":"1394"},{"id":"1457->262905949231132672","targetid":"262905949231132672","sourceid":"1457"},{"id":"2->262905949231132672","targetid":"262905949231132672","sourceid":"2"},{"id":"42->262905949231132672","targetid":"262905949231132672","sourceid":"42"},{"id":"1394->262905949231132672","targetid":"262905949231132672","sourceid":"1394"},{"id":"1457->262905647044104192","targetid":"262905647044104192","sourceid":"1457"},{"id":"2->262905647044104192","targetid":"262905647044104192","sourceid":"2"},{"id":"42->262905647044104192","targetid":"262905647044104192","sourceid":"42"},{"id":"1394->262905647044104192","targetid":"262905647044104192","sourceid":"1394"},{"id":"2->262905593055019008","targetid":"262905593055019008","sourceid":"2"},{"id":"42->262905593055019008","targetid":"262905593055019008","sourceid":"42"},{"id":"2->262902428742062080","targetid":"262902428742062080","sourceid":"2"},{"id":"2->262508122629894144","targetid":"262508122629894144","sourceid":"2"},{"id":"2556->261075460925050880","targetid":"261075460925050880","sourceid":"2556"},{"id":"2556->261067198032928768","targetid":"261067198032928768","sourceid":"2556"},{"id":"2556->261060984322535424","targetid":"261060984322535424","sourceid":"2556"},{"id":"2556->261060871260880896","targetid":"261060871260880896","sourceid":"2556"},{"id":"42->261005483563970560","targetid":"261005483563970560","sourceid":"42"},{"id":"2->260821661954228225","targetid":"260821661954228225","sourceid":"2"}],"texts":[{"text":"#OpenData","id":"2","angle":0},{"text":"#avoindata","id":"1383","angle":0.48332194670612},{"text":"#okfn","id":"24","angle":0.96664389341224},{"text":"#opengov","id":"42","angle":1.4499658401184},{"text":"#job","id":"2560","angle":1.9332877868245},{"text":"#OKF","id":"1618","angle":2.4166097335306},{"text":"#opensustainability","id":"2129","angle":2.8999316802367},{"text":"#OpenParl","id":"1457","angle":3.3832536269429},{"text":"#transparency","id":"1394","angle":3.866575573649},{"text":"#Meemoo","id":"1787","angle":4.3498975203551},{"text":"#opendev","id":"41","angle":4.8332194670612},{"text":"#ogp","id":"1451","angle":5.3165414137673},{"text":"#bigcleancz","id":"2556","angle":5.7998633604735}],"loose":[],"maxLength":169,"minLength":73,"minTime":"10:15pm","minDay":"Tuesday 23","minMonth":"October"}

community_pie_result = [["AL",310504,552339,259034,450818,1231572,1215966,641667],["AK",52083,85640,42153,74257,198724,183159,50277],
                        ["AZ",515910,828669,362642,601943,1804762,1523681,862573],["AR",202070,343207,157204,264160,754420,727124,407205],
                        ["CA",2704659,4499890,2159981,3853788,10604510,8819342,4114496],["CO",358280,587154,261701,466194,1464939,1290094,511094],
                        ["CT",211637,403658,196918,325110,916955,968967,478007],["DE",59319,99496,47414,84464,230183,230528,121688],
                        ["DC",36352,50439,25225,75569,193557,140043,70648],["FL",1140516,1938695,925060,1607297,4782119,4746856,3187797],
                        ["GA",740521,1250460,557860,919876,2846985,2389018,981024],["HI",87207,134025,64011,124834,356237,331817,190067],
                        ["ID",121746,201192,89702,147606,406247,375173,182150],["IL",894368,1558919,725973,1311479,3596343,3239173,1575308],
                        ["IN",443089,780199,361393,605863,1724528,1647881,813839],["IA",201321,345409,165883,306398,750505,788485,444554],
                        ["KS",202529,342134,155822,293114,728166,713663,366706],["KY",284601,493536,229927,381394,1179637,1134283,565867],
                        ["LA",310716,542341,254916,471275,1162463,1128771,540314]]
import pymongo
import urllib
import json
import time
import math
import operator
import codecs

def unix2local(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

connection = pymongo.Connection()
db = connection.admin
db.authenticate('root','root')
db = connection.master_timeline

def person_query(begin=None, end=None, limit=5000000):
    startts = date2ts(begin)
    endts = date2ts(end)
    statuses = db.master_timeline_weibo.find({"timestamp":{"$gte":startts,"$lte":endts},"user.id": 1813080181})
    ts_arr = []
    results = []
    total_keywords_count = {}
    for status in statuses:
        result = {}
        text = status['text']
        text = urllib.quote(text.encode('utf-8'))
        res = urllib.urlopen('http://127.0.0.1:8890/seg?text=%s&f=n,nr,ns,nt' % text)
        data = res.read()
        data = json.loads(data)
        if data['status'] == 'ok':
            result['keywords'] = data['words']
        else:
            print data['status']
            continue
        result['ts'] = status['timestamp']
        for k in result['keywords']:
            if k not in total_keywords_count:
                total_keywords_count[k] = 0
            total_keywords_count[k] += 1
        ts_arr.append(result['ts'])
        results.append(result)
    return ts_arr, results, total_keywords_count

def partition(ts_arr, data, window_size=24*60*60):
    ts_series = []
    ts_start = ts_arr[0]
    ts_end = ts_arr[-1]
    each_step = window_size
    ts_current = ts_start
    data_cursor = -1
    groups_size = []
    groups_keywords_count = []
    while ts_current <= ts_end:
        s_ts = ts_current
        f_ts = ts_current + each_step
        ts_series.append([s_ts, f_ts])
        group = []
        for d in data[data_cursor+1:]:
            ts = d['ts']
            group.append(d)
            if ts >= f_ts:
                break
            data_cursor += 1
        if len(group):
            group_keywords_count = {}
            for d in group:
                for k in d['keywords']:
                    if k not in group_keywords_count:
                        group_keywords_count[k] = 0
                    group_keywords_count[k] += 1
            groups_keywords_count.append(group_keywords_count)
            groups_size.append(len(group))
        ts_current += each_step
    return ts_series, groups_keywords_count, groups_size

def burst(ts_series, groups_keywords_count, total_keywords_count, groups_size, total_size):
    word_burst_in_groups = []
    for period, group_keywords_count, group_size in zip(ts_series, groups_keywords_count, groups_size):
        word_burst_in_group = {}
        for keyword in group_keywords_count.keys():
            A = group_keywords_count[keyword]
            B = total_keywords_count[keyword] - A
            C = group_size - A
            D = total_size - total_keywords_count[keyword] - C
            try:
                word_burst_in_group[keyword] = (A + B + C + D) * ((A*D - B*C) ** 2) * 1.0 / ((A + B) * (C + D) * (A + C) * (B + D))
            except ZeroDivisionError:
                raise
                word_burst_in_group[keyword] = 0
        word_burst_in_groups.append(word_burst_in_group)
    keywords_burst = {}
    for keyword in total_keywords_count.keys():
        for group in word_burst_in_groups:
            if keyword in group:
                if keyword not in keywords_burst:
                    keywords_burst[keyword] = 0
                keywords_burst[keyword] += group[keyword]
    return keywords_burst

def hot(ts_series, groups_keywords_count, total_keywords_count, groups_size):
    word_hot_in_groups = []
    for period, group_keywords_count, group_size in zip(ts_series, groups_keywords_count, groups_size):
        word_hot_in_group = {}
        for keyword in group_keywords_count.keys():
            N = group_keywords_count[keyword]
            word_hot_in_group[keyword] = N * 1.0 / (group_size) 
        word_hot_in_groups.append(word_hot_in_group)
    keywords_hot = {}
    for keyword in total_keywords_count.keys():
        for group in word_hot_in_groups:
            if keyword in group:
                if keyword not in keywords_hot:
                    keywords_hot[keyword] = 0
                keywords_hot[keyword] += group[keyword]
    return keywords_hot
         
        
def personal_cloud():
    time_start = '2012-9-1'
    time_end = '2012-10-1'
    window_size = 24*60*60

    ts_arr, results, total_keywords_count = person_query(begin=time_start, end=time_end)
    total_size = len(results)
    print 'find %s statuses from %s to %s at %s.' % (total_size, time_start, time_end, unix2local(time.time()))
    print ts_arr

    ts_series, groups_keywords_count, groups_size = partition(ts_arr, results, window_size=window_size)
    print 'data partition ok at %s.' % unix2local(time.time())

    keywords_burst = burst(ts_series, groups_keywords_count, total_keywords_count, groups_size, total_size)
    print 'calculate keyword burst ok at %s.' % unix2local(time.time())

    keywords_hot = hot(ts_series, groups_keywords_count, total_keywords_count, groups_size)
    print 'calculate keywork hot ok at %s.' % unix2local(time.time())

    keywords_value = {}
    print keywords_hot
    print keywords_burst
    for keyword in total_keywords_count.keys():
        try:
            keywords_value[keyword] = keywords_hot[keyword] + math.log(keywords_burst[keyword] + 1, 2)
        except KeyError,e:
            continue
    print 'calculate keyword value ok at %s.' % unix2local(time.time())

    keywords_rank_list = sorted(keywords_value.iteritems(), key=operator.itemgetter(1), reverse=True)
    print 'keyword rank ok at %s.' % unix2local(time.time())

    file_url = r'/opt/data/topic/results_%s_%s_%s.txt' % (time_start, time_end, window_size/3600)
    f = codecs.open(file_url, 'w', encoding='utf-8')
    for key, value in keywords_rank_list[:100]:
        f.write('%s %s\n' % (key, value))
    f.close()
    print 'write top 100 results into %s.' % file_url
    
if __name__ == '__main__':personal_cloud()

