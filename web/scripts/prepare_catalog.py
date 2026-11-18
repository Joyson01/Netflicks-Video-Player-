"""Refresh film metadata and licensed artwork from Blender's public sources."""
import requests,json,concurrent.futures,pathlib
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[1]
entries=[
('spring','Spring',2019,'3d95fb3d-c866-42c8-9db1-fe82f48ccb95',['Fantasy','Animation'],'Andy Goralczyk','4.0','A shepherd girl and her loyal dog awaken ancient spirits in a breathtaking journey to bring spring back to a frozen valley.','Some intense scenes'),
('charge','Charge',2022,'04da454b-9893-4184-98f3-248d00625efe',['Sci-Fi','Action'],'Hjalti Hjálmarsson','4.0','In a world running out of power, a desperate man enters a battery factory. A relentless security droid stands between him and his last chance.','Sci-fi violence'),
('wing-it','Wing It!',2023,'bd0084a5-1d26-4816-ab5e-1bad9e2fb990',['Comedy','Animation'],'Rik Schutte','4.0','An exacting engineer. An overenthusiastic pilot. One wildly out-of-control spaceship. Sometimes the best plan is no plan at all.','Cartoon peril'),
('sintel','Sintel',2010,'0eb052d0-fd51-43e6-aa33-ecdbf77a5d40',['Fantasy','Adventure'],'Colin Levy','3.0','A young wanderer travels across a beautiful, unforgiving world in search of the dragon she once rescued. A small act of kindness becomes an extraordinary quest.','Violence and sad themes'),
('big-buck-bunny','Big Buck Bunny',2008,'bf1f3fb5-b119-4f9f-9930-8e20e892b898',['Comedy','Animation'],'Sacha Goedegebure','3.0','A gentle giant enjoys a perfect spring day until three woodland troublemakers push him a little too far. The forest is in for a surprise.','Cartoon violence'),
('coffee-run','Coffee Run',2020,'ff8fe61b-026f-4f07-b66b-2a790d6f6ab1',['Drama','Animation'],'Hjalti Hjálmarsson','4.0','Fueled by caffeine, a young woman races through the bittersweet memories of a past relationship. A whole life, in one extraordinary run.','Relationship themes'),
('tears-of-steel','Tears of Steel',2012,'8533ea43-4271-4a57-9694-e9d0b35e1aa1',['Sci-Fi','Action'],'Ian Hubert','3.0','In a future Amsterdam, a group of scientists and soldiers must revisit a painful memory to stop a robot uprising. Live action meets an imagined world.','Violence and strong language'),
('cosmos-laundromat','Cosmos Laundromat',2015,'f507dfdc-e73e-45a4-9778-d758cbe1ce96',['Fantasy','Drama'],'Mathieu Auvray','3.0','On a lonely island, a sheep gets an unexpected offer: a chance to live another life. But this mysterious deal comes with a time limit.','Mature themes, self-harm imagery and language'),
('caminandes-3','Caminandes: Llamigos',2016,'23f3ef79-15dc-44c5-aa45-cf92e78a4509',['Comedy','Adventure'],'Pablo Vazquez','3.0','Winter in Patagonia. One stubborn llama. One very tempting berry. An unexpected rival turns the hunt for a snack into a lesson in friendship.','Cartoon peril'),
('elephants-dream','Elephants Dream',2006,'cccc3e60-0291-4ecc-aa56-39b2e2c7d0d5',['Sci-Fi','Fantasy'],'Bassam Kurdali','2.5','Two explorers journey through a strange mechanical world. As their ideas about the place diverge, the machinery of their friendship begins to unravel.','Unsettling imagery')]
def prepare(e):
 slug,title,year,uuid,genres,director,license,description,advisory=e
 j=requests.get('https://video.blender.org/api/v1/videos/'+uuid,timeout=30).json()
 files=j['files']
 assert files,slug
 sources=[{'label':f['resolution']['label'],'url':f['fileUrl'],'height':f['height']} for f in files if f['fileUrl'].endswith('.mp4') and f['height']>=360 and f['height']<=1080]
 assert sources,slug
 preferred=min(sources,key=lambda x:abs(x['height']-720))
 r=requests.get(preferred['url'],headers={'Range':'bytes=0-1023'},stream=True,timeout=30);status=r.status_code;r.close();assert status in [200,206],(slug,status)
 page='https://studio.blender.org/projects/'+slug+'/'
 soup=BeautifulSoup(requests.get(page,timeout=30).text,'html.parser')
 image=soup.select_one('meta[property="og:image"]')['content']
 img=requests.get(image,timeout=30);img.raise_for_status();(ROOT/'dist/assets'/f'{slug}.webp').write_bytes(img.content)
 return dict(id=slug,title=title,year=year,duration=j['duration'],genres=genres,director=director,description=description,advisory=advisory,license='CC BY '+license,licenseUrl='https://creativecommons.org/licenses/by/'+license+'/',credit='© Blender Foundation',sourcePage=page,videoPage='https://video.blender.org/w/'+uuid,image='assets/'+slug+'.webp',imageSource=image,sources=sources,defaultSource=preferred['url'])
with concurrent.futures.ThreadPoolExecutor(6) as pool: films=list(pool.map(prepare,entries))
(ROOT/'dist/catalog.json').write_text(json.dumps(films,indent=2,ensure_ascii=False)+'\n')
print('Prepared',len(films),'films. All video sources returned HTTP 200/206.')
