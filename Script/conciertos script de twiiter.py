import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
#ckey = "UvrUEQZpfYHaUtU2cmw1somPl"
#csecret = "Ql34YqGNCwdnd7DG1hv3CgRuayYjC46ItKUuu0WEtw5AiCgBBV"
#atoken = "375942730-51BEzcTtIq5UdQ7kdlHf8W5u4LnkVyXGQl45eSLi"
#asecret = "gn73ZudvSeXrjEneD1dl9gdDr1JCjXLe8guoYRDdvJjL3"

ckey="sgLKYMrlDx11LmQWYQBOPCnK6"
csecret="tNZQMz8s8nN88J3dx8j5mJxE4s2aLxlJHBfZ1lCl1jfjeiW5cl"
atoken="1199828626990125060-OV8usIXq6zH9PJ8gfCfBOFnpjOfbtw"
asecret="gxrNgu0lxkiS0eMwFVeEGDy4xzzpwETkBx2jsmQo4fdwQ"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
#Autenticaciones       
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('conciertos')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['conciertos']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(track=["conciertos","eventos","publico","en","Ecuador"])
#track arreglo de streams
#location con gps
twitterStream.filter(locations=[-1.3397668,-79.3666965])

