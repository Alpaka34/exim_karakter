# stranger_quiz_app.py  # Bu artık "Hangi Kişiye Benziyorsun?" quiz'i için uyarlandı
import streamlit as st
import pandas as pd  # Excel okumak için (ama veri hardcoded, çünkü Streamlit Cloud'da dosya olmayabilir)

st.set_page_config(page_title="Anket - Who R U?", layout="centered")

st.title("📊 Anket: Hangi Kişiye Benziyorsun?")
st.markdown("Aşağıdaki 11 soruya cevap ver, cevaplara göre en uyumlu kişiyi öğren! (Excel verilerine göre puanlama)")

# ────────────────────────────────────────────────
# Veri: Excel'den hardcoded (çünkü Streamlit Cloud'da dosya yüklemek yerine)
# İsimler listesi
isimler = [
    "HAYATİ ÇAYCI", "BATUHAN DURMUŞ", "BURAK KALYONCU", "FATİH ÖZER",
    "MAHMUT GÜLMEZ", "SELAMİ BALCI", "ŞEVKİ BURAK ARDIÇ", "UYGAR DELAL ÇAKMAK",
    "EMRE TIRAŞ", "SERKAN ALTUN", "RAGIP"
]

# Her soru için şıklar ve puanlar (Excel row'larından parse edilmiş)
sorular = [
    {
        "soru": "Yağmurlu bir akşam, yemek siparişimi getiren kuryeye ….",
        "secenekler": [
            "bahşiş veririm.",
            "teşekkür ederim.",
            "muhatap olmam, 'Sağolasın' anlamında başımı sallarım.",
            "ne bahşişi aq!"
        ],
        "puanlar": [  # Her şık için isimlere puan listesi
            [0,2,4,10,10,0,0,10,0,3,10],  # bahşiş veririm
            [0,10,10,5,5,7,10,1,5,10,10],  # teşekkür ederim
            [0,5,8,0,0,4,9,0,10,0,0],      # muhatap olmam
            [10,2,1,0,0,4,0,0,10,0,0]      # ne bahşişi aq
        ]
    },
    {
        "soru": "Mevcut maaşımla, 2 kademe yükselmeyi kabul ….",
        "secenekler": [
            "ederim.",
            "etmem."
        ],
        "puanlar": [
            [0,5,0,10,10,10,4,0,3,0,2],
            [8,5,10,0,0,0,6,10,10,10,10]
        ]
    },
    {
        "soru": "……... olmayı, mevcut maaşımın %20 azına kabul ederim. (Yıllık maaş zamları baki..)",
        "secenekler": [
            "Eximbank GM",
            "Bornova Kaymakamı",
            "Apple Türkiye Direktörü",
            "MİT Sosyal İşler Daire Başkanı",
            "TOKİ Başkanı",
            "Futbol Antrenörü",
            "Marangoz",
            "Otopark sahibi"
        ],
        "puanlar": [
            [0,6,0,10,10,10,0,0,5,0,10],
            [0,10,0,10,10,10,0,0,4,0,0],
            [0,0,0,4,10,0,3,0,8,0,7],
            [0,10,0,10,10,10,4,0,0,0,0],
            [0,2,0,10,10,0,5,0,7,0,5],
            [5,4,0,8,0,0,0,10,10,0,7],
            [2,0,0,0,0,5,0,0,0,8,0],
            [5,0,10,0,0,0,10,10,2,10,6]
        ]
    },
    {
        "soru": "Yaz mevsimine denk gelen kurban bayramında .......",
        "secenekler": [
            "kurban keserim.",
            "vekaletimi verip, yurtiçi tatil yaparım.",
            "vekalet vermem, yurtiçi tatil yaparım.",
            "yurtdışına giderim.",
            "benim ve/veya eşimin akrabalarını ziyaret ederim."
        ],
        "puanlar": [
            [0,3,0,0,4,5,10,0,0,0,0],
            [0,4,0,3,0,3,0,0,0,0,0],
            [10,9,0,5,8,6,6,0,7,0,6],
            [4,0,10,0,0,0,0,10,0,0,0],
            [0,4,0,8,9,8,0,0,0,10,0]
        ]
    },
    {
        "soru": "İnsanlara haftada ortalama …. tane komik reels gönderirim.",
        "secenekler": [
            "göndermem",
            "1--3",
            "4--10",
            "10'dan fazla"
        ],
        "puanlar": [
            [0,0,0,10,0,0,0,0,0,0,0],
            [4,0,10,0,0,5,3,0,2,0,0],
            [0,4,0,0,10,6,0,10,0,0,7],
            [0,0,0,0,0,4,0,0,0,0,0]
        ]
    },
    {
        "soru": "Suriyeliler ??",
        "secenekler": [
            "Doktor ve yazılımcılar dışındakileri gönder.",
            "Sadece erkekleri gönder.",
            "Dini bütün olanları gönder.",
            "Yeni gelenleri alma, kalanlar kalsın.",
            "Hepsini gönder."
        ],
        "puanlar": [
            [4,0,0,7,6,0,10,0,0,0,0],
            [3,0,0,9,0,0,0,0,0,0,0],
            [9,6,0,2,0,0,0,0,0,0,0],
            [7,0,0,0,10,0,5,10,0,0,0],
            [7,9,8,10,3,10,0,0,10,10,10]
        ]
    },
    {
        "soru": "Yılbaşında",
        "secenekler": [
            "Evi süsler çam dikerim.",
            "Evi süsler çam dikmem",
            "Evi süslemem, çam dikmem.",
            "Çam dikmeyi anlamsız bulurum."
        ],
        "puanlar": [
            [5,0,0,10,0,0,6,0,0,0,7],
            [0,0,3,0,0,0,0,0,6,0,2],
            [0,10,0,0,10,5,8,6,5,10,0],
            [0,0,10,0,0,7,9,0,0,0,5]
        ]
    },
    {
        "soru": "….. ideolojisinin kurucu babası olmak isterdim.",
        "secenekler": [
            "Liberalizm",
            "Sosyalizm",
            "Türk Milliyetçiliği",
            "Şeriat",
            "Popülizm",
            "Feminizm",
            "Teknokrasi",
            "Transhümanizm"
        ],
        "puanlar": [
            [3,0,9,0,4,0,0,0,10,6,9],
            [0,0,0,0,6,0,0,8,0,0,0],
            [0,10,0,10,0,10,0,0,0,0,0],
            [0,2,0,0,2,0,10,0,0,0,0],
            [0,4,0,10,5,0,0,0,0,0,0],
            [0,2,0,4,4,0,0,0,0,0,0],
            [9,4,5,1,2,3,0,6,5,0,0],
            [5,3,4,4,6,0,0,7,2,0,0]
        ]
    },
    {
        "soru": "Türkiye'de ilköğrenimin eğitim dili...",
        "secenekler": [
            "Türkçe olmalı",
            "Türkçe ve Kürtçe olmalı",
            "Türkçe, Kürtçe ve Arapça olmalı",
            "Her mikro bölgede ayrı belirlenmeli"
        ],
        "puanlar": [
            [4,8,10,10,0,10,10,10,10,10,10],
            [0,0,0,0,10,0,0,10,0,0,0],
            [0,0,0,0,10,0,0,10,0,0,0],
            [6,0,0,0,8,0,0,10,0,0,0]
        ]
    },
    {
        "soru": "Aralarında en çok şuna gülerim…",
        "secenekler": [
            "Kim götüme elledi benim, hangi şerefsiz?",
            "Evde baktım sadece… attım hafızaya, beyin bedava.",
            "Jamiryo",
            "Artiz ne arar la bazarda",
            "Fuat kurum, murat kavurma, eklem karabulut"
        ],
        "puanlar": [
            [6,6,7,7,7,7,5,10,4,3,2],
            [6,10,7,7,10,7,5,8,4,5,1],
            [6,6,7,7,7,7,8,8,10,7,0],
            [6,6,7,7,6,7,5,8,4,10,0],
            [10,7,10,10,6,9,5,8,4,4,5]
        ]
    },
    {
        "soru": "Yılda kaç kitap okursun?",
        "secenekler": [
            "Hiç yada 1",
            "2--5",
            "5'den fazla"
        ],
        "puanlar": [
            [0,6,10,10,6,6,6,0,10,10,6],
            [9,7,0,3,5,4,4,0,0,0,2],
            [0,0,0,0,0,0,0,10,0,0,0]
        ]
    }
]

# ────────────────────────────────────────────────
# Cevap toplama
cevaplar = []

for i, q in enumerate(sorular, 1):
    secim = st.radio(
        f"{i}. {q['soru']}",
        options=q["secenekler"],
        index=None,
        key=f"q{i}"
    )
    if secim is None:
        cevaplar.append(-1)  # Seçilmemiş
    else:
        cevaplar.append(q["secenekler"].index(secim))

# ────────────────────────────────────────────────
# Hesaplama fonksiyonu
def hesapla_kisi(cevaplar_list):
    puanlar = {isim: 0 for isim in isimler}

    for q_idx, secim_idx in enumerate(cevaplar_list):
        if secim_idx >= 0:
            secim_puanlari = sorular[q_idx]["puanlar"][secim_idx]
            for isim_idx, puan in enumerate(secim_puanlari):
                puanlar[isimler[isim_idx]] += puan

    en_iyi = max(puanlar, key=puanlar.get)
    return en_iyi, puanlar[en_iyi], puanlar

# ────────────────────────────────────────────────
# Buton ve sonuç
if st.button("Sonucumu Göster 🚀", type="primary", use_container_width=True):
    if -1 in cevaplar:
        st.error("Lütfen tüm soruları cevapla!")
    else:
        kisi, puan, tum_puanlar = hesapla_kisi(cevaplar)

        st.success(f"**SEN: {kisi}'ye benziyorsun!**")
        st.markdown(f"**Toplam Puanın:** {puan}")

        st.markdown("### Neden?")
        st.info("Cevapların, bu kişinin puanlarıyla en yüksek uyumu gösterdi. Detaylı puanlar aşağıda.")

        # Tüm puanları göster
        with st.expander("Tüm Kişi Puanları"):

            st.json(tum_puanlar)

