export const resumeTime = p => p && p.time >= 5 && p.time < p.duration * .95 ? p.time : 0;
export function filterFilms(films, query = '', genre = 'All') {
  const q = query.trim().toLocaleLowerCase();
  return films.filter(f => (genre === 'All' || f.genres.includes(genre)) && [f.title, f.description, ...f.genres, f.year].join(' ').toLocaleLowerCase().includes(q));
}
export function createLibrary(storage, films) {
  const ids = new Set(films.map(f => f.id));
  let data = {list: [], progress: {}};
  let persistent = true;
  try {
    const raw = JSON.parse(storage.getItem('netflex:v1') || 'null');
    if (raw && typeof raw === 'object') {
      data.list = Array.isArray(raw.list) ? [...new Set(raw.list.filter(id => ids.has(id)))] : [];
      if (raw.progress && typeof raw.progress === 'object') for (const [id,p] of Object.entries(raw.progress)) {
        if (ids.has(id) && p && Number.isFinite(p.time) && Number.isFinite(p.duration) && p.time >= 0 && p.duration > 0)
          data.progress[id] = {time: Math.min(p.time,p.duration), duration:p.duration, updated:Number(p.updated)||0};
      }
    }
  } catch { /* A damaged record must never stop playback. */ }
  try {storage.setItem('netflex:storage-check','1');storage.removeItem?.('netflex:storage-check');} catch {persistent=false;}
  function save() { try { storage.setItem('netflex:v1', JSON.stringify(data)); } catch { persistent = false; } }
  return {
    get persistent() { return persistent; },
    has: id => data.list.includes(id),
    list: () => data.list.map(id => films.find(f => f.id === id)),
    toggle(id) { if (!ids.has(id)) return; data.list = data.list.includes(id) ? data.list.filter(x => x !== id) : [...data.list,id]; save(); },
    progress: id => data.progress[id],
    record(id,time,duration) { if (!ids.has(id) || !Number.isFinite(time) || !Number.isFinite(duration) || duration <= 0 || time < 0) return; data.progress[id] = {time:Math.min(time,duration),duration,updated:Date.now()};save(); },
    continueWatching: () => films.filter(f => resumeTime(data.progress[f.id]) > 0).sort((a,b)=>data.progress[b.id].updated-data.progress[a.id].updated),
    removeProgress(id) {delete data.progress[id];save();},
    clear() {data={list:[],progress:{}};save();}
  };
}
