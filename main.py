_W='fragments'
_V='format_string'
_U='normal'
_T='ignore'
_S='yt-dlp'
_R='youtube.com'
_Q='disabled'
_P='Hide Library'
_O='Search'
_N='final_filename'
_M='N/A'
_L='artist'
_K='ffmpeg'
_J='.mp3'
_I=None
_H='green'
_G='name'
_F='videoId'
_E='orange'
_D=False
_C='red'
_B='ew'
_A=True
import tkinter
from tkinter import filedialog
import customtkinter,httpx,asyncio,threading,subprocess,os,json,sys,shutil,re
from PIL import Image,ImageTk
API_BASE_URL='YOUR_API_BASE_URL'  # Replace with your actual API base URL
if not API_BASE_URL.startswith('http'):raise ValueError('API_BASE_URL must start with http:// or https://')
SAVE_DIR='spotify_downloads'
COOKIES_FILE_PATH='./conf/cookies.txt'
class App(customtkinter.CTk):
	def __init__(A):
		F='bold';E='transparent';C='icon.png';super().__init__();A.title('Spotify Downloader');A.geometry('700x700');customtkinter.set_appearance_mode('dark');customtkinter.set_default_color_theme(_H)
		try:
			if os.path.exists(C):A.icon_image=ImageTk.PhotoImage(Image.open(C));A.iconphoto(_A,A.icon_image)
		except Exception as D:print(f"Error setting window icon: {D}")
		A.ffmpeg_path=A.get_ffmpeg_path();os.makedirs(SAVE_DIR,exist_ok=_A);os.makedirs(os.path.dirname(COOKIES_FILE_PATH),exist_ok=_A);A.download_queue=[];A.active_process=_I;A.queue_lock=threading.Lock();A.is_processing_queue=_D;A.shutdown_event=threading.Event();A.song_list_visible=_A;A.protocol('WM_DELETE_WINDOW',A.on_closing);A.grid_columnconfigure(0,weight=1);A.grid_rowconfigure(4,weight=1);B=customtkinter.CTkFrame(A,corner_radius=0,fg_color=E);B.grid(row=0,column=0,sticky=_B,padx=20,pady=20);B.grid_columnconfigure(1,weight=1)
		try:
			if os.path.exists(C):G=Image.open(C).resize((40,40));A.logo_image=ImageTk.PhotoImage(G);H=customtkinter.CTkLabel(B,image=A.logo_image,text='');H.grid(row=0,column=0,padx=(0,15))
		except Exception as D:print(f"Could not load header logo: {D}")
		A.header_label=customtkinter.CTkLabel(B,text='Spotify & YouTube Downloader',font=customtkinter.CTkFont(size=24,weight=F));A.header_label.grid(row=0,column=1,sticky='w');A.url_frame=customtkinter.CTkFrame(A);A.url_frame.grid(row=1,column=0,padx=20,pady=(0,10),sticky=_B);A.url_frame.grid_columnconfigure(0,weight=1);A.url_entry=customtkinter.CTkEntry(A.url_frame,placeholder_text='Paste Spotify or YouTube link here...',height=40,font=customtkinter.CTkFont(size=14));A.url_entry.grid(row=0,column=0,padx=10,pady=10,sticky=_B);A.search_button=customtkinter.CTkButton(A.url_frame,text=_O,height=40,font=customtkinter.CTkFont(size=16,weight=F),command=A.start_search_thread);A.search_button.grid(row=0,column=1,padx=(0,5),pady=10);A.ffmpeg_button=customtkinter.CTkButton(A.url_frame,text='Set FFmpeg',height=40,command=A.prompt_for_ffmpeg_path,fg_color='gray50',hover_color='gray30');A.ffmpeg_button.grid(row=0,column=2,padx=(0,10),pady=10);A.progress_frame=customtkinter.CTkFrame(A);A.progress_frame.grid(row=2,column=0,padx=20,pady=5,sticky=_B);A.progress_frame.grid_columnconfigure(0,weight=1);A.analysis_textbox=customtkinter.CTkTextbox(A.progress_frame,height=70,font=customtkinter.CTkFont(family='Arial',size=12),wrap='word',border_width=1);A.analysis_textbox.grid(row=0,column=0,columnspan=2,padx=10,pady=(10,5),sticky=_B);A.update_analysis_text('Analysis results will appear here...');A.bar_cancel_frame=customtkinter.CTkFrame(A.progress_frame,fg_color=E);A.bar_cancel_frame.grid(row=1,column=0,columnspan=2,padx=10,pady=5,sticky=_B);A.bar_cancel_frame.grid_columnconfigure(0,weight=1);A.progress_bar=customtkinter.CTkProgressBar(A.bar_cancel_frame,progress_color='#1DB954');A.progress_bar.set(0);A.progress_bar.grid(row=0,column=0,sticky=_B);A.cancel_button=customtkinter.CTkButton(A.bar_cancel_frame,text='Cancel',width=80,command=A.cancel_all_downloads,fg_color=_C,hover_color='#C0392B');A.cancel_button.grid(row=0,column=1,padx=(10,0));A.status_label=customtkinter.CTkLabel(A.progress_frame,text='',anchor='w');A.status_label.grid(row=2,column=0,columnspan=2,padx=10,pady=(0,10),sticky=_B)
		if not A.ffmpeg_path:A.set_status('WARNING: FFmpeg not found.',_E)
		else:A.set_status(f"FFmpeg found.",_H)
		A.toggle_frame=customtkinter.CTkFrame(A,fg_color=E);A.toggle_frame.grid(row=3,column=0,padx=20,pady=(10,0),sticky=_B);A.toggle_button=customtkinter.CTkButton(A.toggle_frame,text=_P,command=A.toggle_song_list);A.toggle_button.pack(side='left');A.song_list_frame=customtkinter.CTkScrollableFrame(A,label_text='Downloaded Songs',label_font=customtkinter.CTkFont(size=16,weight=F));A.song_list_frame.grid(row=4,column=0,padx=20,pady=5,sticky='nsew');A.load_downloaded_songs()
	def get_ffmpeg_path(D):B='ffmpeg.exe'if sys.platform=='win32'else _K;C=os.path.dirname(sys.executable if getattr(sys,'frozen',_D)else os.path.abspath(__file__));A=os.path.join(C,B);return A if os.path.exists(A)else shutil.which(_K)
	def prompt_for_ffmpeg_path(A):
		B=filedialog.askopenfilename(title='Select FFmpeg Executable')
		if B and _K in os.path.basename(B).lower():A.ffmpeg_path=B;A.set_status(f"FFmpeg path set: {A.ffmpeg_path}",_H)
		elif B:A.set_status('Warning: Selected file might not be FFmpeg.',_E)
	def toggle_song_list(A):
		if A.song_list_visible:A.song_list_frame.grid_remove();A.toggle_button.configure(text='Show Library');A.song_list_visible=_D
		else:A.song_list_frame.grid();A.toggle_button.configure(text=_P);A.song_list_visible=_A
	def start_search_thread(A):threading.Thread(target=lambda:asyncio.run(A.handle_search_press()),daemon=_A).start()
	async def handle_search_press(A):
		F='tracks';B=A.url_entry.get()
		if not B:A.set_status('Please paste a link.',_E);return
		A.set_search_button_state(state=_Q,text='Searching...');A.set_status('Identifying link type...')
		try:
			if'spotify.com'in B:
				A.set_status('Spotify link detected. Contacting API...')
				async with httpx.AsyncClient()as G:E=await G.get(f"{API_BASE_URL}/api/spotify?spotifyUrl={B}",timeout=45.);E.raise_for_status();C=E.json()
				if isinstance(C,list):D=C
				elif isinstance(C,dict)and F in C:D=C[F]
				else:raise ValueError('API response format not recognized.')
				if not D:raise ValueError('API did not return any tracks.')
				A.show_playlist_modal(D)
			elif _R in B or'youtu.be'in B:A.set_status('YouTube link detected. Getting title...');H=[_S,'--get-title',B];I=subprocess.run(H,capture_output=_A,text=_A,encoding='utf-8',errors=_T);J=I.stdout.strip()or'YouTube Video';K={_F:B,_G:J,_L:_I};A.add_tracks_to_queue([K],'bestaudio/best',1)
			else:raise ValueError('Link is not a valid Spotify or YouTube URL.')
		except Exception as L:A.set_status(f"Error: {L}",_C)
		finally:A.set_search_button_state(state=_U,text=_O)
	def show_playlist_modal(E,tracks):
		F=tracks;D='off';A=customtkinter.CTkToplevel(E);A.title('Playlist Tracks');A.geometry('600x550');A.transient(E);A.grab_set();B=customtkinter.CTkFrame(A);B.pack(fill='x',padx=10,pady=10);B.grid_columnconfigure(1,weight=1);B.grid_columnconfigure(3,weight=1);customtkinter.CTkLabel(B,text='Size Limit:').grid(row=0,column=0,padx=(0,5));N=['< 15 MB (Default)','< 50 MB','< 75 MB','< 100 MB','< 150 MB'];I=customtkinter.CTkOptionMenu(B,values=N);I.grid(row=0,column=1,padx=(0,10),sticky=_B);customtkinter.CTkLabel(B,text='Download Parts:').grid(row=0,column=2,padx=(10,5));J=customtkinter.CTkOptionMenu(B,values=['1','2','3','5','10']);J.grid(row=0,column=3,sticky=_B);K=customtkinter.CTkScrollableFrame(A,label_text=f"{len(F)} Tracks Found");K.pack(expand=_A,fill='both',padx=10,pady=(0,10));G=[]
		for H in F:L=tkinter.StringVar(value=D);O=customtkinter.CTkCheckBox(K,text=f"{H.get(_L,_M)} - {H.get(_G,_M)}",variable=L,onvalue=json.dumps(H),offvalue=D);O.pack(anchor='w',padx=10,pady=5);G.append(L)
		C=customtkinter.CTkFrame(A);C.pack(fill='x',padx=10,pady=10);C.grid_columnconfigure((0,1,2),weight=1)
		def M(select=_A):
			for(A,B)in enumerate(G):B.set(json.dumps(F[A])if select else D)
		P=customtkinter.CTkButton(C,text='Select All',command=lambda:M(_A));P.grid(row=0,column=0,padx=5,sticky=_B);Q=customtkinter.CTkButton(C,text='Deselect All',command=lambda:M(_D));Q.grid(row=0,column=1,padx=5,sticky=_B)
		def R():
			B=[json.loads(A.get())for A in G if A.get()!=D];C=I.get();F=int(re.search('\\d+',C).group());H=f"bestaudio[filesize<{F}M]/bestaudio";K=int(J.get())
			if B:E.add_tracks_to_queue(B,H,K);A.destroy()
		S=customtkinter.CTkButton(C,text='Add to Queue',command=R);S.grid(row=0,column=2,padx=5,sticky=_B)
	def add_tracks_to_queue(A,tracks,format_string,fragments):
		G='[\\\\/*?:"<>|]'
		with A.queue_lock:
			C=[]
			for B in tracks:
				F=re.sub(G,'',B.get(_G,'Unknown'));E=B.get(_L)
				if E and E!=_M:H=re.sub(G,'',E);D=f"{H} - {F}.mp3"
				else:D=f"{F}.mp3"
				I=os.path.join(SAVE_DIR,D)
				if not os.path.exists(I):B[_V]=format_string;B[_N]=D;B[_W]=fragments;C.append(B)
				else:print(f"Skipping existing file: {D}")
			if C:A.download_queue.extend(C);A.set_status(f"Added {len(C)} new tracks. {len(A.download_queue)} total pending.");A.start_queue_processing_if_not_running()
			else:A.set_status('All selected tracks already exist.',_H)
	def start_queue_processing_if_not_running(A):
		if not A.is_processing_queue:A.is_processing_queue=_A;threading.Thread(target=A.process_download_queue,daemon=_A).start()
	def process_download_queue(A):
		A.is_processing_queue=_A;C=len(A.download_queue);B=0
		while len(A.download_queue)>0:
			if A.shutdown_event.is_set():break
			with A.queue_lock:D=A.download_queue.pop(0)
			A._download_worker(D);B+=1;E=B/C;A.after(0,A.progress_bar.set,E)
		A.is_processing_queue=_D
		if not A.shutdown_event.is_set():A.set_status('Download queue finished!',_H)
	def _download_worker(A,track):
		B=track;K=threading.get_ident()
		with A.queue_lock:A.active_process=_I
		try:
			D=B[_N];A.set_status(f"Downloading: {D.replace(_J,'')} ({len(A.download_queue)} left)")
			if not A.ffmpeg_path:A.set_status('Error: FFmpeg not found.',_C);return
			E=B.get(_F)if _R not in B.get(_F,'')else B.get(_F)
			if not E:A.set_status(f"Skipping {B.get(_G)}: No YouTube ID.",_E);return
			G=os.path.join(SAVE_DIR,f"{B.get(_F)}.%(ext)s");H=[_S,'--ffmpeg-location',A.ffmpeg_path,'--cookies',COOKIES_FILE_PATH,'-f',B[_V],'-x','--audio-format','mp3','--concurrent-fragments',str(B.get(_W,1)),'--output',G,E];C=subprocess.Popen(H,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=_A,encoding='utf-8',errors=_T,bufsize=1)
			with A.queue_lock:A.active_process=C
			A.update_analysis_text(f"Name: {D.replace(_J,'')}\nSize: Pending...")
			for L in iter(C.stdout.readline,''):
				if A.shutdown_event.is_set():C.terminate();break
			C.wait()
			if A.shutdown_event.is_set():print(f"Download cancelled for {B[_N]}");return
			F=os.path.join(SAVE_DIR,f"{B.get(_F)}.mp3");I=os.path.join(SAVE_DIR,D)
			if C.returncode==0 and os.path.exists(F):shutil.move(F,I);A.after(0,A.load_downloaded_songs)
			else:A.set_status(f"Failed to download {B.get(_G)}",_C)
		except Exception as J:A.set_status(f"Error downloading {B.get(_G)}: {J}",_C)
		finally:
			with A.queue_lock:A.active_process=_I
	def load_downloaded_songs(A):
		for E in A.song_list_frame.winfo_children():E.destroy()
		try:
			F=os.listdir(SAVE_DIR);C=sorted([A for A in F if A.endswith(_J)])
			if not C:customtkinter.CTkLabel(A.song_list_frame,text='No songs downloaded yet.').pack(pady=20);return
			for D in C:G=D.replace(_J,'');B=customtkinter.CTkFrame(A.song_list_frame);B.pack(fill='x',padx=5,pady=5);B.grid_columnconfigure(0,weight=1);customtkinter.CTkLabel(B,text=G,anchor='w').grid(row=0,column=0,padx=10,pady=10,sticky=_B);customtkinter.CTkButton(B,text='▶ Play',width=70,command=lambda p=os.path.join(SAVE_DIR,D):A.play_song(p)).grid(row=0,column=1,padx=10,pady=5)
		except Exception as H:A.set_status(f"Error loading songs: {H}",_C)
	def play_song(B,path):
		A=path
		try:
			if sys.platform=='win32':os.startfile(A)
			elif sys.platform=='darwin':subprocess.call(('open',A))
			else:subprocess.call(('xdg-open',A))
		except Exception as C:B.set_status(f"Could not play file: {C}",_C)
	def set_status(A,text,color='gray'):
		def B():A.status_label.configure(text=text,text_color=color)
		A.after(0,B)
	def set_search_button_state(A,state,text=_I):
		def B():A.search_button.configure(state=state,text=text or A.search_button.cget('text'))
		A.after(0,B)
	def update_analysis_text(A,text):
		def B():B='0.0';A.analysis_textbox.configure(state=_U);A.analysis_textbox.delete(B,'end');A.analysis_textbox.insert(B,text);A.analysis_textbox.configure(state=_Q)
		A.after(0,B)
	def on_closing(A):
		print('Closing application...');A.shutdown_event.set()
		with A.queue_lock:
			if A.active_process:A.active_process.terminate()
			A.download_queue.clear()
		A.destroy()
	def cancel_all_downloads(A):
		B='Cancelling all downloads...';print(B);A.set_status(B,_E);A.shutdown_event.set()
		with A.queue_lock:
			if A.active_process:A.active_process.terminate()
			A.download_queue.clear()
		A.is_processing_queue=_D;A.shutdown_event=threading.Event();A.set_status('Downloads cancelled.',_E);A.after(0,A.progress_bar.set,0);A.after(0,A.percentage_label.configure,{'text':'0%'})
if __name__=='__main__':app=App();app.mainloop()