#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

class KodiFSM(object):
    """Class for getting some basic playing Information from Kodi. It makes
    use of the 'requests'-package."""
    
    def __init__(self, IP_Address='192.168.0.133'):
        """Initiate an instance corresponding to a certain Kodi device on
        the local Network that runs the version 2.0 of the Kodi json API 
        (here it is called "jsonrpc"). If you run Kodi on the same device
        that you run this code on, use the Localhost Address (127.0.0.1). 
        """
        
        """Setup api-endpoint & necessary parameters"""
        self._URL = "http://"+IP_Address+"/jsonrpc"
        self._PARAMS = None
        self._response = None
        self._data = None
        
        """Set a first request to see, if Kodi is online."""
        self._set_request()
        if self._response: print("Kodi available")
        
        """Defining a parameter dict for the parameters to be requestet from the API.
        To be honest, this is the lazy approach, since I put the complete request in one
        string rather than setting up a complete dictionary. Also, most requested parameter are
        not going to be used later on, so I'll have to clear up this part later on."""
        self._Kodi_Get_Player = {'request':'{"jsonrpc":"2.0","id":1,"method":"Player.GetActivePlayers"}'}
        self._Kodi_Get_Audio_Playing = {'request': '{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["runtime","title", "album", "artist", "duration", "thumbnail", "file", "fanart", "streamdetails"], "playerid": 0 }, "id": "AudioGetItem"}'}
        self._Kodi_Get_Audio_Properties = {'request':'{"jsonrpc":"2.0","method":"Player.GetProperties","params":{"properties":["time","percentage","totaltime"],"playerid":0},"id":"AudioGetItem"}'}
        self._Kodi_Get_Video_Playing = {'request':'{"jsonrpc":"2.0","method":"Player.GetItem","params":{"properties":["title","album","artist","showtitle"],"playerid":1},"id":"VideoGetItem"}'}
        self._Kodi_Get_Video_Properties = {'request':'{"jsonrpc":"2.0","method":"Player.GetProperties","params":{"properties":["time","percentage","totaltime"],"playerid":1},"id":"VideoGetItem"}'}
        self._Kodi_Get_Selection = {'request':'{"jsonrpc":"2.0","method":"GUI.GetProperties","params":{"properties":["currentwindow","currentcontrol"]},"id":1}'}
        
        """Initialize the request parameter for the FSM."""
        self._Mode = '_get_player'
        
        """Setup the Output dictionary."""
        self._Output = {}
        self._reset_output()
        
    def _reset_output(self):
        """Reset the Output dictionary to the inital form."""
        self._Output = {'type': 'none',
                        'artist': 'none',
                        'album': 'none',
                        'title': 'Kodi not available.',
                        'window': 'none',
                        'percentage': 0.0,
                        'duration': {},
                        'time': {}}
    
    def _set_request(self):
        """Send the request to Kodi using 'requests' library."""
        try:
            """sending get request and saving the response as response object"""
            self._response = requests.get(url = self._URL, params = self._PARAMS) 
            #print(response.url)
                
            """extracting data in json format"""
            self._data = self._response.json()
            #print(self._data)
        except:
            """raise exception upon error occur and reset initial parameters"""
            print('ERROR: Kodi not available.')
            self._response = 0
            self._data = None
            self._Mode = '_get_player'
    
    def _update(self):
        """Update the FSM and execute the current method."""
        method = getattr(self, self._Mode, lambda: "ERROR: Invalid Method called.")
        return method()
        
    def state(self):
        """Main interaction to the "outside" of the class. Returns the Output-Dict."""
        self._reset_output()
        self._update()
        
        """Make it possible to decide quickly from Output if Kodi is available."""
        return self._Output
            
    def _get_player(self):
        """FSM state. Requests whether audio or video is playing on Kodi."""
        self._PARAMS = self._Kodi_Get_Player 
        self._set_request()
        
        """If Kodi is available and a player is playing: setup next (detailed) request."""
        if self._response and self._data['result'] != []:
            self._Output['type'] = self._data['result'][0]['type']
            
            """set new FSM Mode"""
            self._Mode = '_get_'+self._data['result'][0]['type']+'_playing'
            #print('Execute: ' + self._Mode + '()')
            
            """Execute next FSM Cycle"""
            self._update()
        
        elif self._response == False:
            
            """Return if Kodi is not available."""
            print('ERROR: Response not valid.')
            
        elif self._data['result'] == []:
                        
            """Return Selection if nothing is playing."""
            #print('Nothing playing.')
            
            """set new FSM Mode"""
            self._Mode = '_get_selection'
            #print('Execute: ' + self._Mode + '()')            
            
            """Execute next FSM Cycle"""
            self._update()
            
    def _get_selection(self):
        """FSM state. Requests the current selected control."""
        
        """reset the initial FSM Mode"""
        self._Mode = '_get_player'
        
        """setup parameters and execute request"""
        self._PARAMS = self._Kodi_Get_Selection
        self._set_request()
        
        try:
            """store required information in the Output dictionary"""
            self._Output['type'] = 'selection'
            self._Output['window'] = self._data['result']['currentwindow']['label']
            self._Output['title'] = self._data['result']['currentcontrol']['label']
        
            #print('Selection: ' + self._data['result']['currentcontrol']['label'])
            
        except:
            """raise exception upon error occur and reset initial parameters"""
            try:
                print('ERROR: ' + self._data['error']['message'])
            except:
                print('ERROR: Kodi communication error.')
            self._response = 0
            self._data = None
            self._Mode = '_get_player'
            return
        
    def _get_audio_playing(self):
        """FSM state. Requests detailed information about the audio playing."""
        
        """reset the initial FSM Mode"""
        self._Mode = '_get_player'
        
        """sequently request the different information and store it in local variables."""
        self._PARAMS = self._Kodi_Get_Audio_Playing
        self._set_request()
        audio_info = self._data
        
        self._PARAMS = self._Kodi_Get_Audio_Properties
        self._set_request()
        audio_properties = self._data
        
        #print(audio_info)
        #print(audio_properties)
        
        try:
            """store required information in the Output dictionary"""
            self._Output['artist'] = audio_info['result']['item']['artist']
            self._Output['album'] = audio_info['result']['item']['album']            
            self._Output['title'] = audio_info['result']['item']['label']
            self._Output['percentage'] = audio_properties['result']['percentage']
            self._Output['duration'] = audio_properties['result']['totaltime']
            self._Output['time'] = audio_properties['result']['time']
            
            #print(self._Output)
                   
            #print('Playing: ' + audio_info['result']['item']['label'])
            
        except:
            """raise exception upon error occur and reset initial parameters"""
            try:
                print('ERROR: ' + audio_info['error']['message'])
            except:
                print('ERROR: Kodi communication error.')
            self._response = 0
            self._data = None
            self._Mode = '_get_player'
            return
        
    def _get_video_playing(self):
        """FSM state. Requests detailed information about the video playing."""
        
        """reset the initial FSM Mode"""
        self._Mode = '_get_player'
        
        """sequently request the different information and store it in local variables."""
        self._PARAMS = self._Kodi_Get_Video_Playing
        self._set_request()
        video_info = self._data
        
        self._PARAMS = self._Kodi_Get_Video_Properties
        self._set_request()
        video_properties = self._data
        
        #print(video_info)
        #print(video_properties)
        
        try:
            """store required information in the Output dictionary"""
            #self._Output['artist'] = video_info['result']['item']['artist']
            #self._Output['album'] = video_info['result']['item']['album']            
            self._Output['title'] = video_info['result']['item']['label']
            self._Output['percentage'] = video_properties['result']['percentage']
            self._Output['duration'] = video_properties['result']['totaltime']
            self._Output['time'] = video_properties['result']['time']
            
            #print(self._Output)
            
            #print('Playing: ' + video_info['result']['item']['label'])
        
        except:
            """raise exception upon error occur and reset initial parameters"""
            try:
                print('ERROR: ' + video_info['error']['message'])
            except:
                print('ERROR: Kodi communication error.')
            self._response = 0
            self._data = None
            self._Mode = '_get_player'
            return


