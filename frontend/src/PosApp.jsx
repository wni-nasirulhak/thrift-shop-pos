import React, { useState, useMemo, useEffect, useRef } from 'react'
import { useRenderData } from 'streamlit-component-lib-react-hooks'
import { Streamlit } from 'streamlit-component-lib'
import { Search, ShoppingCart, User, Trash2, Tag, CheckCircle2, X } from 'lucide-react'

// Parse Photo column → first usable image src
// Handles: Cloudinary URL list (JSON), single URL, legacy base64
function getImgSrc(photoField) {
  if (!photoField || photoField === '0' || photoField === 'None') return null
  const s = String(photoField).trim()
  if (s.startsWith('[')) {
    try {
      const urls = JSON.parse(s)
      return urls.length > 0 ? urls[0] : null
    } catch { return null }
  }
  if (s.startsWith('http')) return s
  if (s.length > 100) return `data:image/jpeg;base64,${s}`  // legacy base64
  return null
}

// Cloudinary thumbnail helper
function thumbUrl(src, w = 300) {
  if (!src || !src.includes('cloudinary.com')) return src
  return src.replace('/upload/', `/upload/w_${w},h_${w},c_fill,q_auto/`)
}

export default function PosApp() {
  const renderData = useRenderData()
  const args = renderData.args || {}
  const items = args.inventory || []
  const customers = args.customers || []
  
  const [cart, setCart] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [discountType, setDiscountType] = useState('none')
  const [discountValue, setDiscountValue] = useState(0)
  const [phoneSearch, setPhoneSearch] = useState('')
  const [selectedCustomer, setSelectedCustomer] = useState(null)
  const [usePoints, setUsePoints] = useState(false)
  const [newCustomerName, setNewCustomerName] = useState('')
  const [customerAddress, setCustomerAddress] = useState('')
  const [paymentMethod, setPaymentMethod] = useState('Cash')

  useEffect(() => { Streamlit.setFrameHeight(900) }, [])

  const availableItems = useMemo(() => items.filter(i => i.Status === 'Available'), [items])
  const categories = ['All', ...new Set(availableItems.map(i => i.Category_Name).filter(Boolean))]
  
  const filteredItems = useMemo(() => availableItems.filter(i => {
    const matchSearch = String(i.Item_Name || '').toLowerCase().includes(searchQuery.toLowerCase()) || 
                        String(i.Barcode_ID || '').toLowerCase().includes(searchQuery.toLowerCase())
    return matchSearch && (selectedCategory === 'All' || i.Category_Name === selectedCategory)
  }), [availableItems, searchQuery, selectedCategory])

  const findCustomer = () => {
    const cust = customers.find(c => String(c.Phone_Number) === String(phoneSearch))
    setSelectedCustomer(cust || null)
    setUsePoints(false)
  }

  const addToCart = (item) => {
    if (cart.find(c => c.Barcode_ID === item.Barcode_ID)) return
    setCart(prev => [...prev, { ...item }])
  }
  const removeFromCart = (id) => setCart(prev => prev.filter(c => c.Barcode_ID !== id))

  const subtotal = cart.reduce((sum, item) => sum + (parseFloat(item.Price) || 0), 0)
  let discountAmount = 0
  if (discountType === 'percent') discountAmount = subtotal * (discountValue / 100)
  else if (discountType === 'fixed') discountAmount = Math.min(discountValue, subtotal)
  else if (discountType === 'staff') discountAmount = subtotal * 0.10
  else if (discountType === 'aging') discountAmount = subtotal * 0.30

  let afterDiscount = subtotal - discountAmount
  let pointsDiscount = 0
  if (selectedCustomer && usePoints) {
    const pts = parseInt(selectedCustomer.Points || 0)
    pointsDiscount = Math.min(pts, afterDiscount)
    afterDiscount -= pointsDiscount
  }
  const finalPrice = Math.max(0, afterDiscount)

  const handleCheckout = () => {
    if (cart.length === 0) return
    const checkoutId = `chk_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
    Streamlit.setComponentValue({
      checkoutId, cart,
      customer: selectedCustomer,
      newCustomerName, customerAddress,
      customerPhone: phoneSearch,
      pointsUsed: pointsDiscount,
      discountType,
      discountValue: discountType === 'none' ? 0 : discountValue,
      discountAmount, subtotal, finalPrice, paymentMethod
    })
    setCart([])
    setPhoneSearch('')
    setSelectedCustomer(null)
    setNewCustomerName('')
    setCustomerAddress('')
    setDiscountType('none')
    setDiscountValue(0)
  }

  return (
    <div style={{ fontFamily: "'Prompt','Inter',sans-serif" }} className="flex flex-col md:flex-row w-full bg-slate-50 text-slate-800 gap-3 rounded-xl">
      
      {/* Left: Product Grid */}
      <div className="flex-1 flex flex-col gap-3 min-w-0">
        {/* Search & Filter */}
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-2.5 text-slate-400 w-4 h-4" />
            <input 
              type="text" placeholder="ค้นหาสินค้าหรือบาร์โค้ด..." value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-sm rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-indigo-400 outline-none"
            />
          </div>
          <select value={selectedCategory} onChange={e => setSelectedCategory(e.target.value)}
            className="px-3 py-2 text-sm border border-slate-200 rounded-lg bg-white outline-none">
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        {/* Product Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 overflow-y-auto pr-1" style={{ maxHeight: '760px' }}>
          {filteredItems.map(item => {
            const inCart = cart.some(c => c.Barcode_ID === item.Barcode_ID)
            const imgSrc = getImgSrc(item.Photo)
            return (
              <div key={item.Barcode_ID} onClick={() => addToCart(item)}
                className={`bg-white rounded-xl border p-2 cursor-pointer transition-all flex flex-col select-none
                  ${inCart ? 'border-indigo-500 ring-2 ring-indigo-200 shadow-md' : 'border-slate-100 hover:border-indigo-300 hover:shadow-md'}`}
              >
                <div className="aspect-square bg-slate-100 rounded-lg mb-2 flex items-center justify-center overflow-hidden relative">
                  {imgSrc
                    ? <img src={thumbUrl(imgSrc, 300)} className="object-cover w-full h-full" alt={item.Item_Name}
                        onError={e => { e.target.style.display = 'none' }} />
                    : <Tag className="w-8 h-8 text-slate-300" />
                  }
                  {inCart && (
                    <div className="absolute inset-0 bg-indigo-600/20 flex items-center justify-center">
                      <CheckCircle2 className="w-8 h-8 text-indigo-600" />
                    </div>
                  )}
                </div>
                <div className="text-xs font-semibold leading-tight mb-0.5 line-clamp-2">{item.Item_Name}</div>
                <div className="text-xs text-slate-400">{item.Brand} • {item.Size_Label}</div>
                <div className="text-sm font-bold text-indigo-600 mt-auto pt-1">฿{parseFloat(item.Price || 0).toLocaleString()}</div>
              </div>
            )
          })}
          {filteredItems.length === 0 && (
            <div className="col-span-full py-16 text-center text-slate-400 text-sm">
              <Tag className="w-10 h-10 mx-auto mb-2 opacity-20" />ไม่พบสินค้า
            </div>
          )}
        </div>
      </div>

      {/* Right: Cart Panel */}
      <div className="w-full md:w-[340px] bg-white border border-slate-200 rounded-2xl flex flex-col shadow-sm flex-shrink-0" style={{ maxHeight: '900px' }}>
        
        {/* Header */}
        <div className="p-4 bg-indigo-600 text-white flex items-center justify-between rounded-t-2xl flex-shrink-0">
          <h2 className="font-bold text-base flex items-center gap-2"><ShoppingCart className="w-4 h-4"/> รายการสั่งซื้อ</h2>
          <span className="bg-white/25 px-2 py-0.5 rounded-full text-xs font-semibold">{cart.length} รายการ</span>
        </div>

        <div className="flex-1 overflow-y-auto flex flex-col">
          {/* Customer Section */}
          <div className="p-3 border-b border-slate-100 bg-slate-50/60 flex-shrink-0">
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">ข้อมูลลูกค้า</div>
            <div className="flex gap-2 mb-2">
              <input type="tel" placeholder="เบอร์โทรลูกค้า" value={phoneSearch}
                onChange={e => setPhoneSearch(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && findCustomer()}
                className="flex-1 px-3 py-1.5 text-sm rounded-lg border border-slate-200 outline-none focus:border-indigo-400 bg-white"
              />
              <button onClick={findCustomer} className="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-sm font-semibold hover:bg-indigo-700">ค้นหา</button>
            </div>
            {selectedCustomer ? (
              <div className="flex items-center justify-between bg-emerald-50 text-emerald-700 border border-emerald-200 p-2 rounded-lg mb-2">
                <span className="flex items-center gap-1.5 text-sm font-semibold"><User className="w-4 h-4"/> {selectedCustomer.Customer_Name}</span>
                <span className="text-xs bg-emerald-100 px-2 py-0.5 rounded-full font-bold">{selectedCustomer.Points} pts</span>
              </div>
            ) : phoneSearch && (
              <input type="text" placeholder="ชื่อลูกค้า (เพื่อลงทะเบียนใหม่)" value={newCustomerName}
                onChange={e => setNewCustomerName(e.target.value)}
                className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 outline-none mb-2 focus:border-indigo-400 bg-white"
              />
            )}
            {(selectedCustomer || phoneSearch) && (
              <textarea placeholder="ที่อยู่จัดส่ง (ถ้ามี)" value={customerAddress}
                onChange={e => setCustomerAddress(e.target.value)} rows={2}
                className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 outline-none focus:border-indigo-400 resize-none bg-white"
              />
            )}
            {selectedCustomer && parseInt(selectedCustomer.Points || 0) > 0 && (
              <label className="flex items-center gap-2 mt-2 text-sm text-slate-600 cursor-pointer">
                <input type="checkbox" checked={usePoints} onChange={e => setUsePoints(e.target.checked)} className="rounded accent-indigo-600" />
                <span>ใช้แต้มสะสม <span className="text-indigo-600 font-semibold">(-฿{Math.min(parseInt(selectedCustomer.Points), afterDiscount + pointsDiscount).toLocaleString()})</span></span>
              </label>
            )}
          </div>

          {/* Cart Items */}
          <div className="flex-1 p-3 flex flex-col gap-2">
            {cart.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center py-10 text-slate-300">
                <ShoppingCart className="w-10 h-10 mb-2 opacity-40" />
                <span className="text-sm">ยังไม่มีสินค้าในตะกร้า</span>
              </div>
            ) : cart.map(item => {
              const cartImgSrc = getImgSrc(item.Photo)
              return (
                <div key={item.Barcode_ID} className="flex items-center gap-2 bg-slate-50 rounded-lg p-2">
                  <div className="w-10 h-10 rounded-md overflow-hidden bg-slate-200 flex-shrink-0">
                    {cartImgSrc
                      ? <img src={thumbUrl(cartImgSrc, 80)} className="w-full h-full object-cover" alt="" onError={e => { e.target.style.display='none' }}/>
                      : <Tag className="w-5 h-5 m-auto mt-2.5 text-slate-400" />
                    }
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-semibold truncate">{item.Item_Name}</div>
                    <div className="text-xs text-slate-400">{item.Barcode_ID}</div>
                  </div>
                  <div className="text-sm font-bold text-slate-700 flex-shrink-0">฿{parseFloat(item.Price).toLocaleString()}</div>
                  <button onClick={() => removeFromCart(item.Barcode_ID)} className="text-slate-300 hover:text-red-400 transition-colors p-1 flex-shrink-0">
                    <X className="w-4 h-4" />
                  </button>
                </div>
              )
            })}
          </div>
        </div>

        {/* Footer: Discount + Total + Checkout */}
        <div className="border-t border-slate-100 p-3 bg-slate-50 rounded-b-2xl flex flex-col gap-2 flex-shrink-0">
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 w-16 flex-shrink-0">ส่วนลด</span>
            <select className="flex-1 text-xs bg-white border border-slate-200 rounded-lg px-2 py-1.5 outline-none"
              value={discountType} onChange={e => { setDiscountType(e.target.value); setDiscountValue(0) }}>
              <option value="none">ไม่มี</option>
              <option value="percent">% Off</option>
              <option value="fixed">฿ Off (Fixed)</option>
              <option value="staff">Staff -10%</option>
              <option value="aging">Clearance -30%</option>
            </select>
            {(discountType === 'percent' || discountType === 'fixed') && (
              <input type="number" value={discountValue} min={0}
                onChange={e => setDiscountValue(Number(e.target.value))}
                className="w-16 text-xs px-2 py-1.5 border border-slate-200 rounded-lg text-right outline-none bg-white"
              />
            )}
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 w-16 flex-shrink-0">ชำระ</span>
            <select className="flex-1 text-xs bg-white border border-slate-200 rounded-lg px-2 py-1.5 outline-none"
              value={paymentMethod} onChange={e => setPaymentMethod(e.target.value)}>
              <option value="Cash">💵 เงินสด</option>
              <option value="QR Code">📱 QR Code / PromptPay</option>
              <option value="Card">💳 บัตร</option>
            </select>
          </div>
          <div className="border-t border-slate-200 pt-2 mt-1 flex flex-col gap-1">
            <div className="flex justify-between text-xs text-slate-500">
              <span>ราคารวม</span><span>฿{subtotal.toLocaleString()}</span>
            </div>
            {(discountAmount > 0 || pointsDiscount > 0) && (
              <div className="flex justify-between text-xs text-emerald-600">
                <span>ส่วนลดรวม</span><span>-฿{(discountAmount + pointsDiscount).toLocaleString()}</span>
              </div>
            )}
            <div className="flex justify-between text-lg font-bold mt-1">
              <span>ยอดสุทธิ</span>
              <span className="text-indigo-600">฿{finalPrice.toLocaleString()}</span>
            </div>
          </div>
          <button onClick={handleCheckout} disabled={cart.length === 0}
            className={`w-full py-3 rounded-xl font-bold text-sm text-white flex items-center justify-center gap-2 transition-all
              ${cart.length === 0 ? 'bg-slate-200 text-slate-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 active:scale-[0.98] shadow-lg'}`}>
            <CheckCircle2 className="w-5 h-5"/>
            ยืนยันการขาย ฿{finalPrice.toLocaleString()}
          </button>
        </div>
      </div>
    </div>
  )
}
