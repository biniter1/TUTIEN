export default function DongPhuPage() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="font-display text-3xl text-gold-400 font-bold">Động Phủ</h1>
        <p className="text-slate-500 mt-1 text-sm">Dai ban doanh cua tu tien gia</p>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-navy-800 border border-jade/15 rounded-lg p-5">
          <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Tu Vi</p>
          <p className="text-gold-400 text-2xl font-bold">—</p>
          <p className="text-slate-600 text-xs mt-1">Cultivation Power</p>
        </div>
        <div className="bg-navy-800 border border-jade/15 rounded-lg p-5">
          <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Linh Khi</p>
          <p className="text-jade-400 text-2xl font-bold">—</p>
          <p className="text-slate-600 text-xs mt-1">Spirit Energy</p>
        </div>
        <div className="bg-navy-800 border border-jade/15 rounded-lg p-5">
          <p className="text-slate-500 text-xs uppercase tracking-wider mb-1">Danh Vong</p>
          <p className="text-slate-300 text-2xl font-bold">—</p>
          <p className="text-slate-600 text-xs mt-1">Reputation</p>
        </div>
      </div>

      <div className="bg-navy-800 border border-gold/10 rounded-lg p-6">
        <p className="text-slate-400 text-sm">Noi dung dang duoc xay dung...</p>
      </div>
    </div>
  )
}
