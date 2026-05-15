import pandas as pd   
import matplotlib.pyplot as plt
import os


GECME_NOTU=60
DEVAMSIZ_SINIR=3 

df=pd.read_csv("notlar.csv" , sep=";" ,encoding= "utf-8")
df = df.dropna(subset=["İsim"])

# * ORTALAMA HESAPLAMA FONKSİYONU
def ortalama_hesapla(df):

 return df[["Matematik","Türkçe","Fen"]].mean(axis=1).round(2)  

# * DURUM HESAPLAMA FONKSİYONU
def durum_hesapla(df):
 
 return df["Ortalama"].apply(
    lambda x: "Geçti" if x > GECME_NOTU else "Kaldi"
)

# * DEVAMSIZLIK HESAPLAMA FONKSİYONU
def devamsızlık_durum_hesapla(df):

 return df["Devamsızlık"].apply(
    lambda x : "Riskli" if x >  DEVAMSIZ_SINIR else "Normal"
)

#* FİLTRELEME 
df["Ortalama"]=ortalama_hesapla(df) #* HER ÖĞRENCİNİN ORTALAMASI SÜTUNUNU OLUŞTUR

df["Durum"] = durum_hesapla(df) #* HER ÖĞRENCİNİN DURUMUNU SUTUNUNU OLUŞTUR

df["Devamsızlık_Durumu"]=devamsızlık_durum_hesapla(df) #* HER ÖĞRENCİNİN DEVAMSIZLIK DURUMU SUTUNUNU OLUŞTUR 


 
print("-------ÖĞRENCİ ANALİZİ-------")
print(f"Toplam öğrenci :  {len(df)} ")
print(f"Geçen öğrenciler :{(df["Durum"]=="Geçti").sum()}") #*SUM BUTUN SUTUNU YAZ
print(f"Kalan öğrenciler : {(df["Durum"]=="Kaldi").sum()}") 
print(f"Sinif Ortalaması: {df["Ortalama"].mean():.2f}")
print(f"En yüksek ortalama : {df["Ortalama"].max()}")
print(f"En düşük ortalama : {df["Ortalama"].min()}")


sinif_analiz=df.groupby("sınıf").agg( #! groupby() neye gore sınıflandırıcaksan ona yarar
    ogrenci_sayisi=("İsim","count"), 
    ort_matematik=("Matematik","mean"),
    ort_fen=("Fen","mean"),
    ort_turkce=("Türkçe","mean"),
    ort_genel=("Ortalama","mean")
).round(2)

print(sinif_analiz)

print("-------- RİSKLİ ÖĞRENCİLER --------")
#* KALMA RİSKİ OLAN OĞRENCİ FİLTRESİ
def riskli_hesapla(df):
 return  df[
    (df["Devamsızlık_Durumu"]=="Riskli")|
    (df["Durum"]=="Kaldi")
 ]

riskli = riskli_hesapla(df)

print(riskli[["İsim","sınıf","Ortalama","Devamsızlık"]])

print(df["İsim"])

# TODO:GÖRSELLEŞTİRME YAPILICAK ŞİMDİ

fig ,axes = plt.subplots(2,2,figsize=(14,10))
fig.suptitle("Öğrenci Analiz Raporu",
             fontsize=16 , fontweight="bold")

#*ÖĞRENCİ BAZLI ORTALAMA (Bar)
axes[0,0].bar(df["İsim"],df["Ortalama"],
              color=["green" if d =="Geçti" else "red" for d in df["Durum"]])

axes[0,0].axhline(y=GECME_NOTU , color="black", linestyle="--",label="Geçme Notu")

axes[0,0].set_title("Öğrenci ortalamaları") #*BAŞLIK

axes[0,0].set_ylabel("Ortalama") #*LABEL Y EKSENİ ADI

axes[0,0].tick_params(axis="x",rotation=45) #* X EKSENINDEKİ İSİMLERİ 45 DERECE DONDURUR

axes[0,0].legend() #*AÇIKLAMA KUTUSU OLUŞTURUR

# * DERS BAZLI ORTALAMA (Bar)

ders_ort=df[["Matematik","Türkçe","Fen"]].mean()

axes[0,1].bar(ders_ort.index,ders_ort.values,
              color=["steelblue","salmon","green"])
axes[0,1].set_title("Ders Bazlı Ortalamalar")
axes[0,1].set_ylabel("Ortalama")

#* GEÇTİ / KALDI (Pie)

durum_say=df["Durum"].value_counts()

axes[1,0].pie(durum_say.values,
              labels=durum_say.index,
              autopct="%1.1f%%",
              colors=["green","red"])
axes[1,0].set_title("Geçti Kaldı Dağılımı")

#* SINIF KARŞILAŞTIRMA (Bar)

sınıf_ort=df.groupby("sınıf")["Ortalama"].mean()

axes[1,1].bar(sınıf_ort.index,sınıf_ort.values,
              color=["steelblue","orange"] )

axes[1,1].set_title=("Sınıf Ortalamaları")
axes[1,1].set_ylabel("Ortalama")

plt.tight_layout()  

# TODO:RAPORLAMA : GRAFİĞİ

os.makedirs("rapor", exist_ok=True) #! kaydedilecek dosyayı oluştur
plt.savefig("rapor/grafik.png") #!KAYDET


# TODO:RAPORLAMA : CSV DOSYLARI 

#* TAM TAPOR
df.to_csv("rapor/tam_rapor.csv",index=False,encoding="utf-8-sig", sep=";")  

#* RİSKLİ ÖĞRENCİLER RAPORU
riskli.to_csv("rapor/riskli_ogrenciler.csv",index=False,encoding="utf-8-sig", sep=";")

#* SINIF ANALİZİ
sinif_analiz.to_csv("rapor/sinif_analizi.csv",index=False,encoding="utf-8-sig", sep=";")

print("Raporlar oluşturuldu!")

plt.show()
