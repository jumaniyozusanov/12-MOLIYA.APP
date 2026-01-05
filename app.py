import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
import os


from functools import reduce
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
import string
import pandas as pd 
from openpyxl.cell.cell import MergedCell
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
import tempfile
import os


# ==========================
# EXCEL → PDF FUNKSIYA
# ==========================
from io import BytesIO
from xlsx2html import xlsx2html
import pdfkit
import tempfile
import os

def excel_bytes_to_pdf_bytes(excel_bytes: BytesIO) -> BytesIO:
    """
    Streamlit Cloud / Linux uchun mos Excel → PDF
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        excel_path = os.path.join(tmpdir, "input.xlsx")
        html_path = os.path.join(tmpdir, "output.html")
        pdf_path = os.path.join(tmpdir, "output.pdf")

        # Excel faylni vaqtincha saqlash
        with open(excel_path, "wb") as f:
            f.write(excel_bytes.getbuffer())

        # Excel → HTML
        xlsx2html(excel_path, html_path)

        # HTML → PDF
        pdfkit.from_file(html_path, pdf_path)

        # PDF ni BytesIO ga yuklash
        pdf_buffer = BytesIO()
        with open(pdf_path, "rb") as f:
            pdf_buffer.write(f.read())

        pdf_buffer.seek(0)
        return pdf_buffer


# ==========================
# STREAMLIT ILOVA
# ==========================
st.title("💰 Moliyaviy Hisobot Dasturi")
menu = ["12-Moliya", "Moliya Natija", "Hisobot"]
choice = st.sidebar.selectbox("Sahifa tanlang", menu)

# ==========================
# 12-MOLIYA
# ==========================
if choice == "12-Moliya":
    st.header("📁 12-Moliya uchun fayllarni tanlang")
    katalog1 = st.file_uploader("1-oy katalog", type=["xlsx"])
    baza1 = st.file_uploader("1-oy baza", type=["xlsx"])
    katalog2 = st.file_uploader("2-oy katalog", type=["xlsx"])
    baza2 = st.file_uploader("2-oy baza", type=["xlsx"])
      
    template = st.file_uploader("Shablon", type=["xlsx"])
    output_name = st.text_input("Natija nomi")
    # output_folder = st.text_input("Papka yo'li (masalan C:/Users/User/Desktop)")

    def numeric_like_kivy(df, cols):
        for col in cols:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(",", "", regex=False)
                    .str.strip()
                )
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            return df
           # --- Excelga yozish funksiyasi 
    from openpyxl.styles import Alignment
    from openpyxl.cell.cell import MergedCell
    from openpyxl.utils.dataframe import dataframe_to_rows

    def yoz_sheetga(df, wb, sheet_name, start_row=6, start_col=1):
        if sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
        else:
            ws = wb.create_sheet(sheet_name)

        df = df.reset_index(drop=True)

        for r_idx, row in enumerate(
            dataframe_to_rows(df, index=False, header=False),
            start=start_row
        ):
            for c_idx, value in enumerate(row, start=start_col):
                cell = ws.cell(row=r_idx, column=c_idx)

                if isinstance(cell, MergedCell):
                    continue

                cell.value = value
                cell.alignment = Alignment(wrap_text=True, vertical="top")

                if isinstance(value, (int, float)):
                    cell.number_format = '#,##0.0'


 





    if st.button("START"):
        if katalog1 is None:
            st.error("❌ Katalog1 fayli tanlanmadi")
        elif baza1 is None:
            st.error("❌ Baza1 fayli tanlanmadi")
        elif katalog2 is None:
            st.error("❌ katalog2 fayli tanlanmadi")
        elif baza2 is None:
            st.error("❌ baza2 fayli tanlanmadi")
        elif template is None:
            st.error("❌ Shablon fayli tanlanmadi")
        elif not output_name.strip():
            st.error("❌ Natija nomini kiriting")
        # elif not output_folder.strip():
        #     st.error("❌ Papka yo‘lini kiriting")
        else:
            st.success("✅ Hamma narsa joyida, ishni boshlaymiz")

        # 1️⃣ Excel’larni TO‘G‘RI o‘qish
        katalog08 = pd.read_excel(
            katalog1,
            dtype={"OKPO": str, "SOOGU": str, "OKED": str, "ADRES": str}
        )

        baza08 = pd.read_excel(baza1, dtype={"OKPO": str})

        katalog09 = pd.read_excel(
            katalog2,
            dtype={"OKPO": str, "SOOGU": str, "OKED": str, "ADRES": str}
        )

        baza09 = pd.read_excel(baza2, dtype={"OKPO": str})


        # 2️⃣ FAQAT numeric ustunlar
        baza08 = numeric_like_kivy(
            baza08, ["G1","G2","G3","G4","G5","G6","G7"]
        )
        baza09 = numeric_like_kivy(
            baza09, ["G1","G2","G3","G4","G5","G6","G7"]
        )



        KATALOH08=katalog08[["OKPO","ADRES","SOOGU"]]
        KATALOH08.columns = KATALOH08.columns.str.strip()
        BAZA08=baza08[["OKPO","G1","G2","G3","G4","G5","G6","G7","SATR"]]
        BAZA08.columns=BAZA08.columns.str.strip()
        BAZA08=BAZA08[BAZA08["SATR"]==201]




        JAMI08=pd.merge(BAZA08,KATALOH08,on="OKPO",how="left")
        JAMI08=JAMI08[["SOOGU","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format

        soogu_data = [
            ["00000", "Республика бўйича жами"],
            ["00001", "Айрим вазирлик ва идоралар бўйича"],
            ["04403", "Ўзбекистон Республикаси Қурилиш ва уй-жой коммунал хўжалиги вазирлиги"],
            ["01354", "«Ўзавтосаноат» АЖ"],
            ["08114", "«Ўздонмаҳсулот» АК"],
            ["08654", "«Ўзкимёсаноат» АЖ"],
            ["06264", "«Ўзагротехсаноатхолдинг» АЖ"],
            ["03504", "«Ўзбекистон темир йўллари» АЖ"],
            ["01024", "«Ўзбекнефтгаз» АЖ"],
            ["01124", "«Ҳудудгазтаъминот» АЖ"],
            ["01104", "«Ўзтрансгаз» АЖ"],
            ["06224", "«Ўзпахтасаноат» АЖ"],
            ["01014", "«Ўзбекистон миллий электр тармоқлари» АЖ"],
            ["01074", "«Ҳудудий электр тармоқлари» АЖ"],
            ["01094", "«Иссиқлик электр станциялари» АЖ"],
            ["08524", "Ўзбекистон Республикаси Тоғ-кон саноати ва геология вазирлиги"],
            ["00002", "шу жумладан:"],
            ["06213", "«Олмалиқ кон-металлургия комбинати» АЖ"],
            ["01164", "«Навоий кон-металлургия комбинати» АЖ"],
            ["99999", "Бошқалар"]
        ]

        # --- DataFrame ---
        soogu_df = pd.DataFrame(soogu_data, columns=["SOOGU", "NAIMUZ"])

        # === 1. Asosiy baza (JMAI09) ===
        # JMAI09 = pd.read_excel("JMAI09.xlsx")  # agar fayl bo‘lsa shu yo‘l bilan o‘qisan

        # soogu kodlarini matn sifatida (boshidagi 0 saqlanib) olish
        JAMI08["SOOGU"] = JAMI08["SOOGU"].astype(str).str.zfill(5)

        # === 2. Tartib jadvali (asosiy ro‘yxat) ===
        tartib = [
            ["00000", "Республика бўйича жами"],
            ["00001", "Айрим вазирлик ва идоралар бўйича"],
            ["04403", "Ўзбекистон Республикаси Қурилиш ва уй-жой коммунал хўжалиги вазирлиги"],
            ["01354", "«Ўзавтосаноат» АЖ"],
            ["08114", "«Ўздонмаҳсулот» АК"],
            ["08654", "«Ўзкимёсаноат» АЖ"],
            ["06264", "«Ўзагротехсаноатхолдинг» АЖ"],
            ["03504", "«Ўзбекистон темир йўллари» АЖ"],
            ["01024", "«Ўзбекнефтгаз» АЖ"],
            ["01124", "«Ҳудудгазтаъминот» АЖ"],
            ["01104", "«Ўзтрансгаз» АЖ"],
            ["06224", "«Ўзпахтасаноат» АЖ"],
            ["01014", "«Ўзбекистон миллий электр тармоқлари» АЖ"],
            ["01074", "«Ҳудудий электр тармоқлари» АЖ"],
            ["01094", "«Иссиқлик электр станциялари» АЖ"],
            ["08524", "Ўзбекистон Республикаси Тоғ-кон саноати ва геология вазирлиги"],
            ["00002", "шу жумладан:"],
            ["06213", "«Олмалиқ кон-металлургия комбинати» АЖ"],
            ["01164", "«Навоий кон-металлургия комбинати» АЖ"],
            ["99999", "Бошқалар"]
        ]
        tartib_df = pd.DataFrame(tartib, columns=["SOOGU", "NAIMUZ"])

        # === 3. JMAI09 da soogu bo‘yicha yig‘ish ===
        agg = JAMI08.groupby("SOOGU", as_index=False)[["G1", "G2"]].sum()

        # === 4. Tartib bilan birlashtirish ===
        merged = pd.merge(tartib_df, agg, on="SOOGU", how="left")

        ayrm = ["04403","01354","08114","08654","06264","03504","01024","01124","01104","06224","01014","01074","01094","08524","06213","01164"
                ]

        # === 5. “Айрим вазирлик ва идоралар бўйича” uchun sum ===
        # Bu kodlar “asosiy” ro‘yxatda yo‘q, lekin “idora” sifatida kiritiladi
        boshqamin = ["01144", "04043", "04413", "06184", "07254"]
        ayrim_sum = JAMI08.loc[JAMI08["SOOGU"].isin(ayrm), ["G1", "G2"]].sum()
        merged.loc[merged["SOOGU"] == "00001", ["G1", "G2"]] = ayrim_sum.values

        # === 6. “Республика бўйича жами” uchun barcha yig‘indi ===
        total_sum = JAMI08[["G1", "G2"]].sum()
        merged.loc[merged["SOOGU"] == "00000", ["G1", "G2"]] = total_sum.values

        # === 7. “Бошқалар” uchun qolgan kodlar sum ===
        asosiy_kodlar = tartib_df["SOOGU"].tolist() + boshqamin
        boshqalar_sum = JAMI08.loc[~JAMI08["SOOGU"].isin(asosiy_kodlar), ["G1", "G2"]].sum()
        merged.loc[merged["SOOGU"] == "99999", ["G1", "G2"]] = boshqalar_sum.values

        # === 8. To‘ldirish va yaxlitlash ===
        merged[["G1", "G2"]] = merged[["G1", "G2"]].fillna(0).round(1) / 1000

        # === 9. Yakuniy natija ===
        HISOB08 = merged[["NAIMUZ", "G1", "G2"]]


        HISOB08=HISOB08.replace("0","-")
        wb = load_workbook(template)
        #---------------------------------------------------------------------------------------------------------------------
        ##---------------------------------------------------------------------------------------------------------------------






        KATALOH09=katalog09[["SOOGU","OKPO"]]
        BAZA09=baza09[["OKPO","G1","G2","SATR"]]
        BAZA09=BAZA09[BAZA09["SATR"]==201]

        JAMI09=pd.merge(BAZA09,KATALOH09,on="OKPO",how="left")
        JAMI09=JAMI09[["SOOGU","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format

        # ==============================
        # 1️⃣ Bazani tayyorlash
        # ==============================
        # Masalan: JMAI09 = pd.read_excel("JMAI09.xlsx")
        JAMI09["SOOGU"] = JAMI09["SOOGU"].astype(str).str.zfill(5)

        # ==============================
        # 2️⃣ Asosiy SOOGU ro‘yxati
        # ==============================
        asosiy_kodlar = [
            "01014","01024","01074","01094","01104","01124","01144","01164",
            "01354","03504","04043","04403","04413","06184","06213","06224",
            "06264","07254","08114","08524","08654"
        ]

        # ==============================
        # 3️⃣ Asosiy kodlar bo‘yicha yig‘indi
        # ==============================
        asosiy_sum = (
            JAMI09[JAMI09["SOOGU"].isin(asosiy_kodlar)]
            .groupby("SOOGU", as_index=False)[["G1","G2"]]
            .sum()
        )

        # ==============================
        # 4️⃣ Qolganlarini "Бошқалар"ga yig‘ish
        # ==============================
        boshqalar_sum = (
            JAMI09[~JAMI09["SOOGU"].isin(asosiy_kodlar)][["G1","G2"]]
            .sum()
            .to_frame()
            .T
        )
        boshqalar_sum.insert(0, "SOOGU", "99999")

        # ==============================
        # 5️⃣ Barchasini birlashtirish
        # ==============================
        yakuniy = pd.concat([asosiy_sum, boshqalar_sum], ignore_index=True)

        # Respublika bo‘yicha jami
        res_sum = yakuniy[["G1","G2"]].sum().to_frame().T
        res_sum.insert(0, "SOOGU", "00000")
       

        # Айрим вазирлик ва идоралар бўйича (asosiylar yig‘indisi)
        ayrim_sum = asosiy_sum[["G1","G2"]].sum().to_frame().T
        ayrim_sum.insert(0, "SOOGU", "00001")

        yakuniy = pd.concat([res_sum, ayrim_sum, yakuniy], ignore_index=True)

        # ==============================
        # 6️⃣ Mapping jadvalini yaratamiz
        # ==============================
        mapping_list = [
            ["00000", "Республика бўйича жами"],
            ["00001", "Айрим вазирлик ва идоралар бўйича"],
            ["04403", "Ўзбекистон Республикаси Қурилиш ва уй-жой коммунал хўжалиги вазирлиги"],
            ["01354", "«Ўзавтосаноат» АЖ"],
            ["08114", "«Ўздонмаҳсулот» АК"],
            ["08654", "«Ўзкимёсаноат» АЖ"],
            ["06264", "«Ўзагротехсаноатхолдинг» АЖ"],
            ["03504", "«Ўзбекистон темир йўллари» АЖ"],
            ["01024", "«Ўзбекнефтгаз» АЖ"],
            ["01124", "«Ҳудудгазтаъминот» АЖ"],
            ["01104", "«Ўзтрансгаз» АЖ"],
            ["06224", "«Ўзпахтасаноат» АЖ"],
            ["01014", "«Ўзбекистон миллий электр тармоқлари» АЖ"],
            ["01074", "«Ҳудудий электр тармоқлари» АЖ"],
            ["01094", "«Иссиқлик электр станциялари» АЖ"],
            ["08524", "Ўзбекистон Республикаси Тоғ-кон саноати ва геология вазирлиги"],
            ["00002", "шу жумладан:"],
            ["06213", "«Олмалиқ кон-металлургия комбинати» АЖ"],
            ["01164", "«Навоий кон-металлургия комбинати» АЖ"],
            ["99999", "Бошқалар"]
        ]
        mapping_df = pd.DataFrame(mapping_list, columns=["SOOGU", "NAIMUZ"])

        # ==============================
        # 7️⃣ Mapping bilan birlashtiramiz
        # ==============================
        yakuniy = mapping_df.merge(yakuniy, on="SOOGU", how="left").fillna(0)

        # ==============================
        # 8️⃣ Tartibni mapping_list tartibida saqlaymiz
        # ==============================
        yakuniy["order"] = yakuniy.index
        yakuniy = yakuniy.sort_values("order").drop(columns="order")

        # ==============================
        # 9️⃣ Formatlash va natija
        # ==============================
        yakuniy["G1"] = yakuniy["G1"].round(1)/1000
        yakuniy["G2"] = yakuniy["G2"].round(1)/1000

        pd.set_option('display.float_format', '{:,.1f}'.format)
        HISOB09=yakuniy[[ "NAIMUZ", "G1", "G2"]]


        HISOB=pd.merge(HISOB08,HISOB09,on="NAIMUZ")


        df = HISOB.copy()
        df["G1_Δ"] =  df["G1_y"] - df["G1_x"]
        df["G1_%"] = ((df["G1_x"] / df["G1_y"]) * 100  ).replace([float('inf'), -float('inf')], 0).fillna(0)
        df["G2_Δ"] = df["G2_x"] - df["G2_y"]
        df["G2_%"] = ((df["G2_x"] / df["G2_y"]) * 100 ).replace([float('inf'), -float('inf')], 0).fillna(0)
                # --- 3. Yaxlitlash ---
        # --- 3. Yaxlitlash ---
        for col in ["G1_y", "G1_x", "G1_Δ", "G2_y", "G2_x", "G2_Δ"]:
            df[col] = df[col].round(1)
        for col in ["G1_%", "G2_%"]:
            df[col] = df[col].round(1)

        # --- 4. Ustunlarni tartiblash va nomlash ---
            df_final = df[[
        "NAIMUZ",
        "G1_x", "G1_y", "G1_Δ", "G1_%",
        "G2_x", "G2_y", "G2_Δ", "G2_%"]]
        
        colm = ["G1_x", "G1_y", "G1_Δ", "G1_%",
        "G2_x", "G2_y", "G2_Δ", "G2_%"]
        # df_final = df_final[~(df_final[colm] == 0).all(axis=1)]
        # --- 5. Yakuniy natija ---

        df_final=df_final.set_index("NAIMUZ")
        df_final=df_final.replace("0","-")

        #-------------------------------------------------------------------------------------------------------------------#
        # --------------------------------------------------------------------------------------------------------------------


        #----------------------------------------------------------------------------------------------------------
        #  EXCELGA YOZISHNI BOSHLANISHI 


        # HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH


        KATALOH08=katalog08[["SOOGU","OKPO"]]
        BAZA08=baza08[["OKPO","G1","G2","SATR"]]
        BAZA08_m2=BAZA08[BAZA08["SATR"]==210]

        JAMI08_m2=pd.merge(BAZA08_m2,KATALOH08,on="OKPO",how="left")
        JAMI08_m2=JAMI08_m2[["SOOGU","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format

        # --- DataFrame ---
        soogu_df = pd.DataFrame(soogu_data, columns=["SOOGU", "NAIMUZ"])

        # === 1. Asosiy baza (JMAI09) ===
        # JMAI09 = pd.read_excel("JMAI09.xlsx")  # agar fayl bo‘lsa shu yo‘l bilan o‘qisan

        # soogu kodlarini matn sifatida (boshidagi 0 saqlanib) olish
        JAMI08_m2["SOOGU"] = JAMI08_m2["SOOGU"].astype(str).str.zfill(5)


        tartib_df = pd.DataFrame(tartib, columns=["SOOGU", "NAIMUZ"])

        # === 3. JMAI09 da soogu bo‘yicha yig‘ish ===
        agg_m2 = JAMI08_m2.groupby("SOOGU", as_index=False)[["G1", "G2"]].sum()

        # === 4. Tartib bilan birlashtirish ===
        merged_m2 = pd.merge(tartib_df, agg_m2, on="SOOGU", how="left")

        # === 5. “Айрим вазирлик ва идоралар бўйича” uchun sum ===
        # Bu kodlar “asosiy” ro‘yxatda yo‘q, lekin “idora” sifatida kiritiladi
        boshqamin = ["01144", "04043", "04413", "06184", "07254"]
        ayrim_sum_m2 = JAMI08_m2.loc[JAMI08_m2["SOOGU"].isin(boshqamin), ["G1", "G2"]].sum()
        merged_m2.loc[merged_m2["SOOGU"] == "00001", ["G1", "G2"]] = ayrim_sum_m2.values

        # === 6. “Республика бўйича жами” uchun barcha yig‘indi ===
        total_sum_m2 = JAMI08_m2[["G1", "G2"]].sum()
        merged_m2.loc[merged_m2["SOOGU"] == "00000", ["G1", "G2"]] = total_sum_m2.values

        # === 7. “Бошқалар” uchun qolgan kodlar sum ===
        asosiy_kodlar = tartib_df["SOOGU"].tolist() + boshqamin
        boshqalar_sum_m2 = JAMI08_m2.loc[~JAMI08_m2["SOOGU"].isin(asosiy_kodlar), ["G1", "G2"]].sum()
        merged_m2.loc[merged_m2["SOOGU"] == "99999", ["G1", "G2"]] = boshqalar_sum_m2.values

        # === 8. To‘ldirish va yaxlitlash ===
        merged_m2[["G1", "G2"]] = merged_m2[["G1", "G2"]].fillna(0).round(1) / 1000

        # === 9. Yakuniy natija ===
        HISOB08_m2 = merged_m2[["NAIMUZ", "G1", "G2"]]

        #---------------------------------------------------------------------------------------------------------------------
        ##---------------------------------------------------------------------------------------------------------------------






        KATALOH09=katalog09[["SOOGU","OKPO"]]
        BAZA09=baza09[["OKPO","G1","G2","SATR"]]
        BAZA09_m2=BAZA09[BAZA09["SATR"]==210]

        JAMI09_m2=pd.merge(BAZA09_m2,KATALOH09,on="OKPO",how="left")
        JAMI09_m2=JAMI09_m2[["SOOGU","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format

        # ==============================
        # 1️⃣ Bazani tayyorlash
        # ==============================
        # Masalan: JMAI09 = pd.read_excel("JMAI09.xlsx")
        JAMI09_m2["SOOGU"] = JAMI09_m2["SOOGU"].astype(str).str.zfill(5)




        # ==============================
        # 3️⃣ Asosiy kodlar bo‘yicha yig‘indi
        # ==============================
        asosiy_sum_m2 = (
            JAMI09_m2[JAMI09_m2["SOOGU"].isin(asosiy_kodlar)]
            .groupby("SOOGU", as_index=False)[["G1","G2"]]
            .sum()
        )

        # ==============================
        # 4️⃣ Qolganlarini "Бошқалар"ga yig‘ish
        # ==============================
        boshqalar_sum_m2 = (
            JAMI09_m2[~JAMI09_m2["SOOGU"].isin(asosiy_kodlar)][["G1","G2"]]
            .sum()
            .to_frame()
            .T
        )
        boshqalar_sum_m2.insert(0, "SOOGU", "99999")

        # ==============================
        # 5️⃣ Barchasini birlashtirish
        # ==============================
        yakuniy_t = pd.concat([asosiy_sum_m2, boshqalar_sum_m2], ignore_index=True)

        # Respublika bo‘yicha jami
        res_sum_ = yakuniy_t[["G1","G2"]].sum().to_frame().T
        res_sum_.insert(0, "SOOGU", "00000")

        # Айрим вазирлик ва идоралар бўйича (asosiylar yig‘indisi)
        ayrim_sum_m2 = asosiy_sum_m2[["G1","G2"]].sum().to_frame().T
        ayrim_sum_m2.insert(0, "SOOGU", "00001")

        yakuniy_t = pd.concat([res_sum_, ayrim_sum_m2, yakuniy_t], ignore_index=True)


        mapping_df_m2 = pd.DataFrame(mapping_list, columns=["SOOGU", "NAIMUZ"])

        # ==============================
        # 7️⃣ Mapping bilan birlashtiramiz
        # ==============================
        yakuniy_t = mapping_df_m2.merge(yakuniy_t, on="SOOGU", how="left").fillna(0)

        # ==============================
        # 8️⃣ Tartibni mapping_list tartibida saqlaymiz
        # ==============================
        yakuniy_t["order"] = yakuniy_t.index
        yakuniy_t = yakuniy_t.sort_values("order").drop(columns="order")

        # ==============================
        # 9️⃣ Formatlash va natija
        # ==============================
        yakuniy_t["G1"] = yakuniy_t["G1"].round(1)/1000
        yakuniy_t["G2"] = yakuniy_t["G2"].round(1)/1000

        pd.set_option('display.float_format', '{:,.1f}'.format)
        HISOB09_m2=yakuniy_t[[ "NAIMUZ", "G1", "G2"]]


        HISOB_m2=pd.merge(HISOB08_m2,HISOB09_m2,on="NAIMUZ")


        df = HISOB_m2.copy()

        df["G1_Δ"] = df["G1_x"] - df["G1_y"]
        df["G1_%"] = ((df["G1_x"] / df["G1_y"]) * 100  ).replace([float('inf'), -float('inf')], 0).fillna(0)
        df["G2_Δ"] = df["G2_x"] - df["G2_y"]
        df["G2_%"] = ((df["G2_x"] / df["G2_y"]) * 100 ).replace([float('inf'), -float('inf')], 0).fillna(0)

        # --- 3. Yaxlitlash ---
        for col in ["G1_y", "G1_x", "G1_Δ", "G2_y", "G2_x", "G2_Δ"]:
            df[col] = df[col].round(1)
        for col in ["G1_%", "G2_%"]:
            df[col] = df[col].round(1)

        # --- 4. Ustunlarni tartiblash va nomlash ---
        df_final_2 = df[[
        "NAIMUZ",
        "G1_x", "G1_y", "G1_Δ", "G1_%",
        "G2_x", "G2_y", "G2_Δ", "G2_%"]]
       
        colm = ["G1_x", "G1_y", "G1_Δ", "G1_%",
        "G2_x", "G2_y", "G2_Δ", "G2_%"]
        df_final_2 = df_final_2[~(df_final_2[colm] == 0).all(axis=1)]
        # --- 5. Yakuniy natija ---

        df_final_2=df_final_2.set_index("NAIMUZ")
        df_final_2=df_final_2.replace("0","-")



        # yoz_sheetga(df_final, "кредитор-по министр", start_row=9, start_col=2)

        # 4️⃣ Faylni faqat 1 MARTA saqlaymiz
     
        print("✅ кредитор-по министр sheetga yozildi!")




        # Viloyat boyisha debitor===================================================================================================




        # katalog07=katalog08
        # baza07=baza08

        KAT08=katalog08[["ADRES","OKPO"]]
        KAT08["ADRES"]=KAT08["ADRES"].str.split(",").str[0]
        KAT08.columns=KAT08.columns.str.strip().str.upper()
        KAT08["ADRES"] = KAT08["ADRES"].str.replace("`", "'", regex=False).str.lower().str.strip()

        KAT08.columns=KAT08.columns.str.strip().str.upper()




        BAZ08=baza08[["OKPO","SATR","G1","G2"]]
        BAZ08=BAZ08[BAZ08["SATR"]==201]
        pd.set_option('display.float_format', '{:,.0f}'.format)
        #BAZA07.groupby("soato_4")[["g1","g2"]].sum()
        BAZ08.columns=BAZ08.columns.str.strip().str.upper()

        mer=pd.merge(BAZ08,KAT08,on="OKPO",how="left")



        pd.set_option('display.float_format', '{:,.0f}'.format)
        HAM08=mer.groupby("ADRES")[["G1","G2"]].sum()/ 1_000
        pd.options.display.float_format = '{:,.1f}'.format
        HAM08
#       BU YERDA 08 UN GRUP BY QILINDI TAYYOR


        KAT09=katalog09[["OKPO","ADRES"]]
        BAZ09=baza09[["OKPO","G1","G2","SATR"]]

        BAZ09=BAZ09[BAZ09["SATR"]==201]

        KAT09["ADRES"]=KAT09["ADRES"].str.split(",").str[0]
        KAT09.columns=KAT09.columns.str.strip().str.upper()
        KAT09["ADRES"] = KAT09["ADRES"].str.replace("`", "'", regex=False).str.lower().str.strip()


        JAM=pd.merge(BAZ09,KAT09,on="OKPO",how="left")
        JAM=JAM[["ADRES","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format


        HAM09=JAM.groupby("ADRES")[["G1","G2"]].sum()/1000
        pd.options.display.float_format = '{:,.1f}'.format
        HAM09

        HAMMASI=pd.merge(HAM08,HAM09,on="ADRES")
        
        
        HAMMASI
        # BU YERGACHA HAMMASI  ADRES KESMIDA BIRIKDI 

        pd.set_option('display.float_format', '{:,.1f}'.format)

        # 1️⃣ Farq va foizlarni hisoblash
        HAMMASI = HAMMASI.copy()
        HAMMASI['G1_diff'] = HAMMASI['G1_y'] - HAMMASI['G1_x']
        HAMMASI['G1_pct'] = (HAMMASI['G1_diff'] / HAMMASI['G1_x'] * 100).round(1)+100
        HAMMASI['G2_diff'] = HAMMASI['G2_y'] - HAMMASI['G2_x']
        HAMMASI['G2_pct'] = (HAMMASI['G2_diff'] / HAMMASI['G2_x'] * 100).round(1)+100

        # 2️⃣ Ustunlar tartibi
        HAMMASI = HAMMASI[['G1_x','G1_y','G1_diff','G1_pct','G2_x','G2_y','G2_diff','G2_pct']]

        # 3️⃣ Ўзбекистон Республикаси yig‘indisi
        uz_sum = pd.DataFrame(HAMMASI.sum()).T
        uz_sum.index = ["O'zbekiston Respublikasi"]
        uz_sum['G1_pct'] = (uz_sum['G1_y'] / uz_sum['G1_x'] * 100).round(1)
        uz_sum['G2_pct'] = (uz_sum['G2_y'] / uz_sum['G2_x'] * 100).round(1)

        # 4️⃣ Barchasini birlashtirish
        DEB_VILOYAT = pd.concat([uz_sum, HAMMASI])

        # 5️⃣ Tartib bo‘yicha viloyatlar
        viloyat_tartib = [
            "O'zbekiston Respublikasi",
            "qoraqalpog'iston respublikasi",
            "viloyatlar",
            "andijon viloyati",
            "buxoro viloyati",
            "jizzax viloyati",
            "qashqadaryo viloyati",
            "navoiy viloyati",
            "namangan viloyati",
            "samarqand viloyati",
            "surxondaryo viloyati",
            "sirdaryo viloyati",
            "toshkent viloyati",
            "farg'ona viloyati",
            "xorazm viloyati",
            "toshkent shahri"
        ]

        DEB_VILOYAT = DEB_VILOYAT.reindex(viloyat_tartib)

        # 6️⃣ Ustun nomlari
       
        colm = ['G1_x','G1_y','G1_diff','G1_pct','G2_x','G2_y','G2_diff','G2_pct']
        # DEB_VILOYAT = DEB_VILOYAT[~(DEB_VILOYAT[colm] == 0).all(axis=1)]
        # 7️⃣ Natija
        #HISOB_FINAL.to_excel("hisob0809_krit.xlsx")
        DEB_VILOYAT=DEB_VILOYAT.replace("0","-")

        # yoz_sheetga(HISOB_FINAL,"дебитор-по обл",start_row=8,start_col=2)
        # print("✅ дебитор-по обл sheetga yozildi!")


        # Viloyat boyisha kreditor ===================================================================================================






        KAT08=katalog08[["ADRES","OKPO"]]
        KAT08["ADRES"]=KAT08["ADRES"].str.split(",").str[0]
        KAT08.columns=KAT08.columns.str.strip().str.upper()
        KAT08["ADRES"] = KAT08["ADRES"].str.replace("`", "'", regex=False).str.lower().str.strip()

        KAT08.columns=KAT08.columns.str.strip().str.upper()




        BAZ08_m=baza08[["OKPO","SATR","G1","G2"]]
        BAZ08_m=BAZ08_m[BAZ08_m["SATR"]==210]
        pd.set_option('display.float_format', '{:,.0f}'.format)
        #BAZA07.groupby("soato_4")[["g1","g2"]].sum()
        BAZ08_m.columns=BAZ08_m.columns.str.strip().str.upper()

        mer_m=pd.merge(BAZ08_m,KAT08,on="OKPO",how="left")



        pd.set_option('display.float_format', '{:,.0f}'.format)
        HAM08_m=mer_m.groupby("ADRES")[["G1","G2"]].sum()/ 1_000
        pd.options.display.float_format = '{:,.1f}'.format
        HAM08_m
#       BU YERDA 08 UN GRUP BY QILINDI TAYYOR


        KAT09=katalog09[["OKPO","ADRES"]]
        BAZ09_m=baza09[["OKPO","G1","G2","SATR"]]

        BAZ09_m=BAZ09_m[BAZ09_m["SATR"]==210]

        KAT09["ADRES"]=KAT09["ADRES"].str.split(",").str[0]
        KAT09.columns=KAT09.columns.str.strip().str.upper()
        KAT09["ADRES"] = KAT09["ADRES"].str.replace("`", "'", regex=False).str.lower().str.strip()


        JAM_m=pd.merge(BAZ09_m,KAT09,on="OKPO",how="left")
        JAM_m=JAM_m[["ADRES","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format


        HAM09_m=JAM_m.groupby("ADRES")[["G1","G2"]].sum()/1000
        pd.options.display.float_format = '{:,.1f}'.format
        HAM09_m

        HAMMASI_m=pd.merge(HAM08_m,HAM09_m,on="ADRES")
        
        
        HAMMASI_m
        # BU YERGACHA HAMMASI  ADRES KESMIDA BIRIKDI 

        pd.set_option('display.float_format', '{:,.1f}'.format)

        # 1️⃣ Farq va foizlarni hisoblash
        HAMMASI_m = HAMMASI_m.copy()
        HAMMASI_m['G1_diff'] = HAMMASI_m['G1_y'] - HAMMASI_m['G1_x']
        HAMMASI_m['G1_pct'] = (HAMMASI_m['G1_diff'] / HAMMASI_m['G1_x'] * 100).round(1)+100
        HAMMASI_m['G2_diff'] = HAMMASI_m['G2_y'] - HAMMASI_m['G2_x']
        HAMMASI_m['G2_pct'] = (HAMMASI_m['G2_diff'] / HAMMASI_m['G2_x'] * 100).round(1)+100

        # 2️⃣ Ustunlar tartibi
        HAMMASI_m = HAMMASI_m[['G1_x','G1_y','G1_diff','G1_pct','G2_x','G2_y','G2_diff','G2_pct']]

        # 3️⃣ Ўзбекистон Республикаси yig‘indisi
        uz_sum_m = pd.DataFrame(HAMMASI_m.sum()).T
        uz_sum_m.index = ["O'zbekiston Respublikasi"]
        uz_sum_m['G1_pct'] = (uz_sum_m['G1_y'] / uz_sum_m['G1_x'] * 100).round(1)
        uz_sum_m['G2_pct'] = (uz_sum_m['G2_y'] / uz_sum_m['G2_x'] * 100).round(1)

        # 4️⃣ Barchasini birlashtirish
        KIR_VILOYAT = pd.concat([uz_sum_m, HAMMASI_m])

        # 5️⃣ Tartib bo‘yicha viloyatlar
        viloyat_tartib = [
            "O'zbekiston Respublikasi",
            "qoraqalpog'iston respublikasi",
            "viloyatlar",
            "andijon viloyati",
            "buxoro viloyati",
            "jizzax viloyati",
            "qashqadaryo viloyati",
            "navoiy viloyati",
            "namangan viloyati",
            "samarqand viloyati",
            "surxondaryo viloyati",
            "sirdaryo viloyati",
            "toshkent viloyati",
            "farg'ona viloyati",
            "xorazm viloyati",
            "toshkent shahri"
        ]

        KIR_VILOYAT = KIR_VILOYAT.reindex(viloyat_tartib)

        # 6️⃣ Ustun nomlari
       
        colm = ['G1_x','G1_y','G1_diff','G1_pct','G2_x','G2_y','G2_diff','G2_pct']
        # KIR_VILOYAT = KIR_VILOYAT[~(KIR_VILOYAT[colm] == 0).all(axis=1)]
        # 7️⃣ Natija
        #HISOB_FINAL.to_excel("hisob0809_krit.xlsx")
        KIR_VILOYAT=KIR_VILOYAT.replace("0","-")

        # yoz_sheetga(HISOB_FINAL,"дебитор-по обл",start_row=8,start_col=2)
        # print("✅ дебитор-по обл sheetga yozildi!")

        # Zarar viloyat boyicha ============================================================================================




        KATALOG09=katalog09[["OKPO","ADRES"]]
        BAZA09=baza09[["OKPO","G1","G2","SATR"]]
        KATALOG09["ADRES"] = KATALOG09["ADRES"].str.replace("`", "'", regex=False).str.lower().str.strip()


        #-----------------------------------------------------------------------------------------------------------
        import pandas as pd

        # 1️⃣ 102 va 103 satrlarni ajratamiz
        BAZA09_102 = BAZA09[BAZA09["SATR"] == 102]
        BAZA09_103 = BAZA09[BAZA09["SATR"] == 103]

        # 2️⃣ Har ikkalasini KATALOH bilan bog‘laymiz
        KATALOG09["ADRES"] = KATALOG09["ADRES"].str.split(",").str[0]

        JAMI_102 = pd.merge(BAZA09_102, KATALOG09, on="OKPO", how="left")[["ADRES", "G2"]]
        JAMI_103 = pd.merge(BAZA09_103, KATALOG09, on="OKPO", how="left")[["ADRES", "G2"]]



        JAMI102 = (
            JAMI_102.groupby("ADRES", as_index=False)
                .agg(
                    G2_SUM_1000_102=("G2", lambda x: x.sum() / 1000),
                    G2_COUNT_102=("G2", lambda x: (x > 0).sum())
                )
        )



        JAMI103 = (
            JAMI_103.groupby("ADRES", as_index=False)
                .agg(
                    G2_SUM_1000_103=("G2", lambda x: x.sum() / 1000),
                    G2_COUNT_103=("G2", lambda x: (x > 0).sum())
                )
        )


        # 4️⃣ Endi ikkisini ADRES bo‘yicha birlashtiramiz
        JAMI_MERGED = pd.merge(JAMI103, JAMI102, on="ADRES", how="outer")

        # 5️⃣ Ko‘rinishni chiroyli qilish
        pd.options.display.float_format = '{:,.1f}'.format

        # === Sizdagi asosiy jadval ===
        # JAMI_MERGED mavjud deb olinadi

        # 1️⃣ Viloyatlar tartibi
        viloyat_tartib = [
            "Ўзбекистон Республикаси",
            "qoraqalpog'iston respublikasi",
            "viloyatlar",
            "andijon viloyati",
            "buxoro viloyati",
            "jizzax viloyati",
            "qashqadaryo viloyati",
            "navoiy viloyati",
            "namangan viloyati",
            "samarqand viloyati",
            "surxondaryo viloyati",
            "sirdaryo viloyati",
            "toshkent viloyati",
            "farg'ona viloyati",
            "xorazm viloyati",
            "toshkent shahri"
        ]

        # 2️⃣ Farq va foiz ustunlarini hisoblaymiz
        JAMI_MERGED["COUNT_DIFF"] = JAMI_MERGED["G2_COUNT_102"] - JAMI_MERGED["G2_COUNT_103"]
        JAMI_MERGED["SUM_DIFF_1000"] = JAMI_MERGED["G2_SUM_1000_102"] - JAMI_MERGED["G2_SUM_1000_103"]

        # Nolga bo‘lishni oldini olish
        JAMI_MERGED["SUM_RATIO_PERCENT"] = (
            (JAMI_MERGED["G2_SUM_1000_102"] / JAMI_MERGED["G2_SUM_1000_103"]) * 100
        ).replace([float('inf'), -float('inf')], pd.NA)

        # 3️⃣ Umumiy yig‘indi satr ("Ўзбекистон Республикаси")
        sum_row = pd.DataFrame({
            "ADRES": ["Ўзбекистон Республикаси"],
            "G2_COUNT_103": [JAMI_MERGED["G2_COUNT_103"].sum()],
            "G2_COUNT_102": [JAMI_MERGED["G2_COUNT_102"].sum()],
            "COUNT_DIFF": [JAMI_MERGED["COUNT_DIFF"].sum()],
            "G2_SUM_1000_103": [JAMI_MERGED["G2_SUM_1000_103"].sum()],
            "G2_SUM_1000_102": [JAMI_MERGED["G2_SUM_1000_102"].sum()],
            "SUM_DIFF_1000": [JAMI_MERGED["SUM_DIFF_1000"].sum()],
            "SUM_RATIO_PERCENT": [
                (JAMI_MERGED["G2_SUM_1000_102"].sum() / JAMI_MERGED["G2_SUM_1000_103"].sum()) * 100
            ]
        })

        # 4️⃣ Barchasini birlashtiramiz
        JAMI_ub = pd.concat([sum_row, JAMI_MERGED], ignore_index=True)

        colm = ['G2_COUNT_103','G2_COUNT_102','COUNT_DIFF','G2_SUM_1000_103','G2_SUM_1000_102'
                ,'SUM_DIFF_1000','SUM_RATIO_PERCENT']
        # JAMI_ub = JAMI_ub[~(JAMI_ub[colm] == 0).all(axis=1)]

        JAMI_ub=JAMI_ub.set_index("ADRES")
        JAMI_ub=JAMI_ub.reindex(viloyat_tartib).replace("0","-")
        JAMI_ub=JAMI_ub.replace("0","-")



        # yoz_sheetga(JAMI_ub,"обл убытка",start_row=5,start_col=2)
        print("✅ обл убытка  sheetga yozildi!")

        #  Zarar vazirlik boyicha ==========================================================================================




        KATALOH09=katalog09[["SOOGU","OKPO"]]
        BAZA09=baza09[["OKPO","G1","G2","SATR"]]

        BAZA09=BAZA09[BAZA09["SATR"]==102]

        JAMI09=pd.merge(BAZA09,KATALOH09,on="OKPO",how="left")
        JAMI09=JAMI09[["SOOGU","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format

        # 1️⃣ Ma'lumotlarni tayyorlash
        KATALOH09 = katalog09[["SOOGU", "OKPO"]].copy()
        BAZA09 = baza09[["OKPO", "G1", "G2", "SATR"]].copy()

        # 2️⃣ Kodlar formatini to‘g‘rilash
        KATALOH09["SOOGU"] = KATALOH09["SOOGU"].astype(str).str.zfill(5)


        # 4️⃣ Hisoblash funksiyasi
        def hisobla(df, satr):
            B = df[df["SATR"] == satr]
            J = pd.merge(B, KATALOH09, on="OKPO", how="left")[["SOOGU", "G2"]]

            asosiy = (
                J[J["SOOGU"].isin(asosiy_kodlar)]
                .groupby("SOOGU", as_index=False)
                .agg(
                    SUM=("G2", lambda x: x.sum() / 1000),
                    COUNT=("G2", lambda x: (x > 0).sum())
                )
            )

            boshqalar = J[~J["SOOGU"].isin(asosiy_kodlar)]
            boshqalar_agg = pd.DataFrame({
                "SOOGU": ["99999"],
                "SUM": [boshqalar["G2"].sum() / 1000],
                "COUNT": [(boshqalar["G2"] > 0).sum()]
            })

            jami = pd.concat([asosiy, boshqalar_agg], ignore_index=True)

            # Айрим вазирлик ва идоралар бўйича (asosiy yig‘indisi)
            ayrim_sum_ = pd.DataFrame({
                "SOOGU": ["00001"],
                "SUM": [asosiy["SUM"].sum()],
                "COUNT": [asosiy["COUNT"].sum()]
            })

            # Ўзбекистон Республикаси бўйича жами
            total = pd.DataFrame({
                "SOOGU": ["00000"],
                "SUM": [jami["SUM"].sum()],
                "COUNT": [jami["COUNT"].sum()]
            })

            jami = pd.concat([total, ayrim_sum_, jami], ignore_index=True)
            return jami

        # 5️⃣ 102 va 103 uchun hisoblash
        res102 = hisobla(BAZA09, 102).rename(columns={"SUM": "G2_SUM_1000_102", "COUNT": "G2_COUNT_102"})
        res103 = hisobla(BAZA09, 103).rename(columns={"SUM": "G2_SUM_1000_103", "COUNT": "G2_COUNT_103"})

        # 6️⃣ Birlashtirish
        yakuniy_v = pd.merge(res102, res103, on="SOOGU", how="outer").fillna(0)

        # 7️⃣ Qo‘shimcha ustunlar (farq va foiz)
        yakuniy_v["COUNT_DIFF"] = yakuniy_v["G2_COUNT_102"].astype(int) - yakuniy_v["G2_COUNT_103"].astype(int)
        yakuniy_v["SUM_DIFF"] = yakuniy_v["G2_SUM_1000_102"] - yakuniy_v["G2_SUM_1000_103"]
        yakuniy_v["SUM_PCT"] = yakuniy_v.apply(
            lambda x: (x["G2_SUM_1000_102"] / x["G2_SUM_1000_103"] * 100) if x["G2_SUM_1000_103"] != 0 else 0,
            axis=1
        ).round(1)

        # 8️⃣ Tartib va nomlar
        tartib = [
            ["00000", "Ўзбекистон Республикаси"],
            ["00001", "Айрим вазирлик ва идоралар бўйича"],
            ["04403", "Ўзбекистон Республикаси Қурилиш ва уй-жой коммунал хўжалиги вазирлиги"],
            ["01354", "«Ўзавтосаноат» АЖ"],
            ["08114", "«Ўздонмаҳсулот» АК"],
            ["08654", "«Ўзкимёсаноат» АЖ"],
            ["06264", "«Ўзагротехсаноатхолдинг» АЖ"],
            ["03504", "«Ўзбекистон темир йўллари» АЖ"],
            ["01024", "«Ўзбекнефтгаз» АЖ"],
            ["01124", "«Ҳудудгазтаъминот» АЖ"],
            ["01104", "«Ўзтрансгаз» АЖ"],
            ["06224", "«Ўзпахтасаноат» АЖ"],
            ["01014", "«Ўзбекистон миллий электр тармоқлари» АЖ"],
            ["01074", "«Ҳудудий электр тармоқлари» АЖ"],
            ["01094", "«Иссиқлик электр станциялари» АЖ"],
            ["08524", "Ўзбекистон Республикаси Тоғ-кон саноати ва геология вазирлиги"],
            # ["00002", "шу жумладан:"],
            
            ["99999", "Бошқалар"]
        ]

        tartib_df = pd.DataFrame(tartib, columns=["SOOGU", "НАИМ"])
        yakuniy_v = pd.merge(tartib_df, yakuniy_v, on="SOOGU", how="left").fillna(0)

        # 9️⃣ Ustunlarni nomlash
        yakuniy_v = yakuniy_v[
            ["НАИМ",
            "G2_COUNT_103","G2_COUNT_102","COUNT_DIFF",
            "G2_SUM_1000_103","G2_SUM_1000_102","SUM_DIFF","SUM_PCT"]
        ]

        # 10️⃣ Formatlash
        yakuniy_v = yakuniy_v.round(1)
        pd.set_option('display.float_format', '{:,.1f}'.format)

        colm = ["G2_COUNT_103","G2_COUNT_102","COUNT_DIFF",
            "G2_SUM_1000_103","G2_SUM_1000_102","SUM_DIFF","SUM_PCT"]
        # yakuniy_v = yakuniy_v[~(yakuniy_v[colm] == 0).all(axis=1)]

        yakuniy_v=yakuniy_v.set_index("НАИМ")
        yakuniy_v=yakuniy_v.replace("0","-")

        # yoz_sheetga(yakuniy_v,"минс убытка",start_row=6,start_col=2)
        print("✅ минс убытка sheetga yozildi!")

        # # TAB 1 ===============================================================================================================


        KATALOG09=katalog09[["OKPO","ADRES"]]
        BAZA09=baza09[["OKPO","G1","G2","SATR"]]

        #BAZA09=BAZA09[BAZA09["SATR"]==210]

        KATALOG09["ADRES"]=KATALOG09["ADRES"].str.split(",").str[0]
        KATALOG09.columns=KATALOG09.columns.str.strip().str.upper()
        KATALOG09["ADRES"] = KATALOG09["ADRES"].str.replace("`", "'", regex=False).str.lower().str.strip()


        JAMI=pd.merge(BAZA09,KATALOG09,on="OKPO",how="left")
        JAMI=JAMI[["ADRES","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format
        JAMI







        BAZA09_201=BAZA09[BAZA09["SATR"]==201]
        BAZA09_202 = BAZA09[BAZA09["SATR"] == 202]
        BAZA09_203 = BAZA09[BAZA09["SATR"] == 203]
        BAZA09_204 = BAZA09[BAZA09["SATR"] == 204]
        BAZA09_205 = BAZA09[BAZA09["SATR"] == 205]

        # 2️⃣ Har ikkalasini KATALOH bilan bog‘laymiz
        KATALOG09["ADRES"] = KATALOG09["ADRES"].str.split(",").str[0]
        JAMI_201 = pd.merge(BAZA09_201, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_202 = pd.merge(BAZA09_202, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_203 = pd.merge(BAZA09_203, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_204 = pd.merge(BAZA09_204, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_205 =pd.merge(BAZA09_205, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]

        hisob_201=JAMI_201.groupby("ADRES")["G1"].sum().reset_index()
        hisob_202=JAMI_202.groupby("ADRES")["G1"].sum().reset_index()
        hisob_203=JAMI_203.groupby("ADRES")["G1"].sum().reset_index()
        hisob_204=JAMI_204.groupby("ADRES")["G1"].sum().reset_index()
        hisob_205=JAMI_205.groupby("ADRES")["G1"].sum().reset_index()




        # Misol uchun: 5 ta df bor
        dfs = [hisob_201,hisob_202,hisob_203,hisob_204,hisob_205]

        # Har bir df’da G1 ustun nomini noyob qilish
        for i, df in enumerate(dfs, start=1):
            df.rename(columns={"G1": f"G1_{i}"}, inplace=True)

        # Hammasini 'ADRES' bo‘yicha birlashtirish
        yakuniy1 = reduce(lambda left, right: pd.merge(left, right, on="ADRES", how="outer"), dfs)

        # Natija
        yakuniy1["G_6"]=yakuniy1["G1_1"]-yakuniy1["G1_5"]
        yakuniy1

        yakuniy1=yakuniy1.set_index("ADRES")


        yakuniy1= yakuniy1.reindex(viloyat_tartib)
        yakuniy1

        # 1️⃣ Hammasini yig‘amiz (NaN'larni hisobdan chiqarib)
        summalar = yakuniy1.sum(numeric_only=True)

        # 2️⃣ "Ўзбекистон Республикаси" qatori uchun yig‘indini qo‘yamiz
        yakuniy1.loc["Ўзбекистон Республикаси"] = summalar
        yakuniy1/1000
        pd.options.display.float_format = '{:,.1f}'.format
        YAKUN1=yakuniy1/1000
        colm = ["G1_1","G1_2","G1_3","G1_4","G1_5","G_6"]
        # YAKUN1 = YAKUN1[~(YAKUN1[colm] == 0).all(axis=1)]

        YAKUN1=YAKUN1.replace("0","-")

        
        print("✅ таб 1 sheetga yozildi!")


        # TAB 3 ================================================================================================================




        KATALOG09=katalog09[["OKPO","ADRES"]]
        BAZA09=baza09[["OKPO","G1","G2","SATR"]]

        #BAZA09=BAZA09[BAZA09["SATR"]==210]

        KATALOG09["ADRES"]=KATALOG09["ADRES"].str.split(",").str[0]
        KATALOG09.columns=KATALOG09.columns.str.strip().str.upper()
        KATALOG09["ADRES"] = KATALOG09["ADRES"].str.replace("`", "'", regex=False).str.lower().str.strip()


        JAMI=pd.merge(BAZA09,KATALOG09,on="OKPO",how="left")
        JAMI=JAMI[["ADRES","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format
        JAMI





        BAZA09_210 = BAZA09[BAZA09["SATR"] == 210]
        BAZA09_211 = BAZA09[BAZA09["SATR"] == 211]
        BAZA09_212 = BAZA09[BAZA09["SATR"] == 212]
        BAZA09_213 = BAZA09[BAZA09["SATR"] == 213]
        BAZA09_214 = BAZA09[BAZA09["SATR"] == 214]
        BAZA09_215 = BAZA09[BAZA09["SATR"] == 215]
        BAZA09_216 = BAZA09[BAZA09["SATR"] == 216]
        BAZA09_218 = BAZA09[BAZA09["SATR"] == 218]


        # 2️⃣ Har ikkalasini KATALOH bilan bog‘laymiz
        KATALOG09["ADRES"] = KATALOG09["ADRES"].str.split(",").str[0]
        JAMI_210 = pd.merge(BAZA09_210, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_211 = pd.merge(BAZA09_211, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_212 = pd.merge(BAZA09_212, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_213 = pd.merge(BAZA09_213, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_214 = pd.merge(BAZA09_214, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_215 =pd.merge(BAZA09_215, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_216 = pd.merge(BAZA09_216, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]
        JAMI_218 = pd.merge(BAZA09_218, KATALOG09, on="OKPO", how="left")[["ADRES", "G1"]]

        hisob_210=JAMI_210.groupby("ADRES")["G1"].sum().reset_index()
        hisob_211=JAMI_211.groupby("ADRES")["G1"].sum().reset_index()
        hisob_212=JAMI_212.groupby("ADRES")["G1"].sum().reset_index()
        hisob_213=JAMI_213.groupby("ADRES")["G1"].sum().reset_index()
        hisob_214=JAMI_214.groupby("ADRES")["G1"].sum().reset_index()
        hisob_215=JAMI_215.groupby("ADRES")["G1"].sum().reset_index()
        hisob_216=JAMI_216.groupby("ADRES")["G1"].sum().reset_index()
        hisob_218=JAMI_218.groupby("ADRES")["G1"].sum().reset_index()



        # Misol uchun: 5 ta df bor
        dfs = [hisob_210,hisob_211,hisob_212,hisob_213,hisob_214,hisob_215,hisob_216,hisob_218]

        # Har bir df’da G1 ustun nomini noyob qilish
        for i, df in enumerate(dfs, start=1):
            df.rename(columns={"G1": f"G1_{i}"}, inplace=True)

        # Hammasini 'ADRES' bo‘yicha birlashtirish
        yakuniy3 = reduce(lambda left, right: pd.merge(left, right, on="ADRES", how="outer"), dfs)

        yakuniy3
        # Natija
        yakuniy3["G_9"]=yakuniy3["G1_1"]-yakuniy3["G1_7"]
        yakuniy3

        yakuniy3=yakuniy3.set_index("ADRES")


        yakuniy3 = yakuniy3.reindex(viloyat_tartib)
        yakuniy3

        # 1️⃣ Hammasini yig‘amiz (NaN'larni hisobdan chiqarib)
        summalar = yakuniy3.sum(numeric_only=True)

        # 2️⃣ "Ўзбекистон Республикаси" qatori uchun yig‘indini qo‘yamiz
        yakuniy3.loc["Ўзбекистон Республикаси"] = summalar
        yakuniy3/1000
        pd.options.display.float_format = '{:,.1f}'.format
        YAKUN3=yakuniy3/1000

        colm = ["G1_1","G1_2","G1_3","G1_4","G1_5","G1_6","G1_7","G1_8","G_9"]
        # YAKUN3 = YAKUN3[~(YAKUN3[colm] == 0).all(axis=1)]

        YAKUN3=YAKUN3.replace("0","-")
        # yoz_sheetga(YAKUN,"таб 3",start_row=7,start_col=2)
        print("✅ таб 3 sheetga yozildi!")

        #  TAB 5 ============================================================================================================






        KATALOH09=katalog09[["SOOGU","OKPO"]]
        BAZA09=baza09[["OKPO","G1","SATR"]]
        KATALOH09.loc[:,"SOOGU"] = KATALOH09["SOOGU"].astype(str).str.zfill(5)

        BAZA_201=BAZA09[BAZA09["SATR"]==201]
        BAZA_202=BAZA09[BAZA09["SATR"]==202]
        BAZA_203=BAZA09[BAZA09["SATR"]==203]
        BAZA_204=BAZA09[BAZA09["SATR"]==204]
        BAZA_205=BAZA09[BAZA09["SATR"]==205]

        JAMI201=pd.merge(BAZA_201,KATALOH09,on="OKPO",how="left")
        JAMI202=pd.merge(BAZA_202,KATALOH09,on="OKPO",how="left")
        JAMI203=pd.merge(BAZA_203,KATALOH09,on="OKPO",how="left")
        JAMI204=pd.merge(BAZA_204,KATALOH09,on="OKPO",how="left")
        JAMI205=pd.merge(BAZA_205,KATALOH09,on="OKPO",how="left")

        pd.options.display.float_format = '{:,.1f}'.format
        JAMI_201=JAMI201[["SOOGU","G1"]]
        JAMI_202=JAMI202[["SOOGU","G1"]]
        JAMI_203=JAMI203[["SOOGU","G1"]]
        JAMI_204=JAMI204[["SOOGU","G1"]]
        JAMI_205=JAMI205[["SOOGU","G1"]]


        import pandas as pd

        # === SOOGU nomlari ro‘yxati (faqat 1 marta yoziladi) ===
        tartib = [
            ["00000", "Республика бўйича жами"],
            ["00001", "Айрим вазирлик ва идоралар бўйича"],
            ["04403", "Ўзбекистон Республикаси Қурилиш ва уй-жой коммунал хўжалиги вазирлиги"],
            ["01354", "«Ўзавтосаноат» АЖ"],
            ["08114", "«Ўздонмаҳсулот» АК"],
            ["08654", "«Ўзкимёсаноат» АЖ"],
            ["06264", "«Ўзагротехсаноатхолдинг» АЖ"],
            ["03504", "«Ўзбекистон темир йўллари» АЖ"],
            ["01024", "«Ўзбекнефтгаз» АЖ"],
            ["01124", "«Ҳудудгазтаъминот» АЖ"],
            ["01104", "«Ўзтрансгаз» АЖ"],
            ["06224", "«Ўзпахтасаноат» АЖ"],
            ["01014", "«Ўзбекистон миллий электр тармоқлари» АЖ"],
            ["01074", "«Ҳудудий электр тармоқлари» АЖ"],
            ["01094", "«Иссиқлик электр станциялари» АЖ"],
            ["08524", "Ўзбекистон Республикаси Тоғ-кон саноати ва геология вазирлиги"],
            ["00002", "шу жумладан:"],
            ["06213", "«Олмалиқ кон-металлургия комбинати» АЖ"],
            ["01164", "«Навоий кон-металлургия комбинати» АЖ"],
            ["99999", "Бошқалар"]
        ]

        tartib_df = pd.DataFrame(tartib, columns=["SOOGU", "NAIMUZ"])

        # Idoralar ro‘yxati (har safar ishlatiladi)
        ayrm = ["04403","01354","08114","08654","06264","03504","01024","01124","01104","06224","01014","01074","01094","08524","06213","01164"
        ]
        boshqamin=["01144", "04043", "04413", "06184", "07254"]
        # === FUNKSIYA: Har bir SATR (201, 202, …) bo‘yicha hisoblash ===
        def hisobla(df):
            df = df.copy()
            df["SOOGU"] = df["SOOGU"].astype(str).str.zfill(5)

            # 1. SOOGU bo‘yicha yig‘ish
            agg = df.groupby("SOOGU", as_index=False)["G1"].sum()

            # 2. Tartib bilan birlashtirish
            merged = pd.merge(tartib_df, agg, on="SOOGU", how="left")

            # 3. “Айрим вазирлик ва идоралар бўйича”
            ayrim_sum = df.loc[df["SOOGU"].isin(ayrm), "G1"].sum()
            merged.loc[merged["SOOGU"] == "00001", "G1"] = ayrim_sum

            # 4. “Республика бўйича жами”
            total_sum = df["G1"].sum()
            merged.loc[merged["SOOGU"] == "00000", "G1"] = total_sum

            # 5. “Бошқалар”
            asosiy_kodlar = tartib_df["SOOGU"].tolist() + boshqamin
            boshqalar_sum = df.loc[~df["SOOGU"].isin(asosiy_kodlar), "G1"].sum()
            merged.loc[merged["SOOGU"] == "99999", "G1"] = boshqalar_sum

            # 6. To‘ldirish va 1000 ga bo‘lish
            merged["G1"] = merged["G1"].fillna(0).round(1) / 1000

            # 7. Yakuniy natija
            result = merged[["NAIMUZ", "G1"]].set_index("NAIMUZ")
            return result
        HISOB_201 = hisobla(JAMI_201)
        HISOB_202 = hisobla(JAMI_202)
        HISOB_203 = hisobla(JAMI_203)
        HISOB_204 = hisobla(JAMI_204)
        HISOB_205 = hisobla(JAMI_205)

        from functools import reduce

        dfs = [HISOB_201, HISOB_202, HISOB_203, HISOB_204, HISOB_205]

        # Har bir df’da G1 nomini noyob qilish
        for i, df in enumerate(dfs, start=1):
            df.rename(columns={"G1": f"G1_{i}"}, inplace=True)
            if "NAIMUZ" in df.columns:
                df.set_index("NAIMUZ", inplace=True)

        # Join orqali birlashtirish
        yakuniy = reduce(lambda left, right: left.join(right, how="outer"), dfs)

        # 🔥 Eng muhim qadam — tartibni tiklash
        yakuniy = yakuniy.reindex(HISOB_201.index)

        # Yangi ustun qo‘shish
        yakuniy["G_6"] = yakuniy["G1_1"] - yakuniy["G1_5"]

        yakuniy

        colm = ["G1_1","G1_2","G1_3","G1_4","G1_5","G_6"]
        # yakuniy1 = yakuniy1[~(yakuniy1[colm] == 0).all(axis=1)]


        yakuniy1=yakuniy.replace("0","-")


        print("✅ таб 5 sheetga yozildi!")


        # TAB 7 ==============================================================================================================





        KATALOH09=katalog09[["SOOGU","OKPO"]]
        BAZA09=baza09[["OKPO","G1","SATR"]]
        KATALOH09["SOOGU"] = KATALOH09["SOOGU"].astype(str).str.zfill(5)

        BAZA_210=BAZA09[BAZA09["SATR"]==210]
        BAZA_211=BAZA09[BAZA09["SATR"]==211]
        BAZA_212=BAZA09[BAZA09["SATR"]==212]
        BAZA_213=BAZA09[BAZA09["SATR"]==213]
        BAZA_214=BAZA09[BAZA09["SATR"]==214]
        BAZA_215=BAZA09[BAZA09["SATR"]==215]
        BAZA_216=BAZA09[BAZA09["SATR"]==216]
        BAZA_218=BAZA09[BAZA09["SATR"]==218]

        JAMI210=pd.merge(BAZA_210,KATALOH09,on="OKPO",how="left")
        JAMI211=pd.merge(BAZA_211,KATALOH09,on="OKPO",how="left")
        JAMI212=pd.merge(BAZA_212,KATALOH09,on="OKPO",how="left")
        JAMI213=pd.merge(BAZA_213,KATALOH09,on="OKPO",how="left")
        JAMI214=pd.merge(BAZA_214,KATALOH09,on="OKPO",how="left")
        JAMI215=pd.merge(BAZA_215,KATALOH09,on="OKPO",how="left")
        JAMI216=pd.merge(BAZA_216,KATALOH09,on="OKPO",how="left")
        JAMI218=pd.merge(BAZA_218,KATALOH09,on="OKPO",how="left")

        pd.options.display.float_format = '{:,.1f}'.format

        JAMI_210=JAMI210[["SOOGU","G1"]]
        JAMI_211=JAMI211[["SOOGU","G1"]]
        JAMI_212=JAMI212[["SOOGU","G1"]]
        JAMI_213=JAMI213[["SOOGU","G1"]]
        JAMI_214=JAMI214[["SOOGU","G1"]]
        JAMI_215=JAMI215[["SOOGU","G1"]]
        JAMI_216=JAMI216[["SOOGU","G1"]]
        JAMI_218=JAMI218[["SOOGU","G1"]]

        #------------------------------------------------------------------------------------------------------------------


        tartib = [
            ["00000", "Республика бўйича жами"],
            ["00001", "Айрим вазирлик ва идоралар бўйича"],
            ["04403", "Ўзбекистон Республикаси Қурилиш ва уй-жой коммунал хўжалиги вазирлиги"],
            ["01354", "«Ўзавтосаноат» АЖ"],
            ["08114", "«Ўздонмаҳсулот» АК"],
            ["08654", "«Ўзкимёсаноат» АЖ"],
            ["06264", "«Ўзагротехсаноатхолдинг» АЖ"],
            ["03504", "«Ўзбекистон темир йўллари» АЖ"],
            ["01024", "«Ўзбекнефтгаз» АЖ"],
            ["01124", "«Ҳудудгазтаъминот» АЖ"],
            ["01104", "«Ўзтрансгаз» АЖ"],
            ["06224", "«Ўзпахтасаноат» АЖ"],
            ["01014", "«Ўзбекистон миллий электр тармоқлари» АЖ"],
            ["01074", "«Ҳудудий электр тармоқлари» АЖ"],
            ["01094", "«Иссиқлик электр станциялари» АЖ"],
            ["08524", "Ўзбекистон Республикаси Тоғ-кон саноати ва геология вазирлиги"],
            ["00002", "шу жумладан:"],
            ["06213", "«Олмалиқ кон-металлургия комбинати» АЖ"],
            ["01164", "«Навоий кон-металлургия комбинати» АЖ"],
            ["99999", "Бошқалар"]
        ]

        tartib_df = pd.DataFrame(tartib, columns=["SOOGU", "NAIMUZ"])

        # Idoralar ro‘yxati (har safar ishlatiladi)
        ayrm = ["04403","01354","08114","08654","06264","03504","01024","01124","01104","06224","01014","01074","01094","08524","06213","01164"
        ]
        boshqamin=["01144", "04043", "04413", "06184", "07254"]
        #----------------------------------------------------------------
        def hisobla(df):
            df = df.copy()
            df.loc[:,"SOOGU"] = df["SOOGU"].astype(str).str.zfill(5)

            # 1. SOOGU bo‘yicha yig‘ish
            agg = df.groupby("SOOGU", as_index=False)["G1"].sum()

            # 2. Tartib bilan birlashtirish
            merged = pd.merge(tartib_df, agg, on="SOOGU", how="left")

            # 3. “Айрим вазирлик ва идоралар бўйича”
            ayrim_sum = df.loc[df["SOOGU"].isin(ayrm), "G1"].sum()
            merged.loc[merged["SOOGU"] == "00001", "G1"] = ayrim_sum

            # 4. “Республика бўйича жами”
            total_sum = df["G1"].sum()
            merged.loc[merged["SOOGU"] == "00000", "G1"] = total_sum

            # 5. “Бошқалар”
            asosiy_kodlar = tartib_df["SOOGU"].tolist() + boshqamin
            boshqalar_sum = df.loc[~df["SOOGU"].isin(asosiy_kodlar), "G1"].sum()
            merged.loc[merged["SOOGU"] == "99999", "G1"] = boshqalar_sum

            # 6. To‘ldirish va 1000 ga bo‘lish
            merged["G1"] = merged["G1"].fillna(0).round(1) / 1000

            # 7. Yakuniy natija
            result = merged[["NAIMUZ", "G1"]].set_index("NAIMUZ")
            return result

        HISOB_210=hisobla(JAMI_210)
        HISOB_211=hisobla(JAMI_211)
        HISOB_212=hisobla(JAMI_212)
        HISOB_213=hisobla(JAMI_213)
        HISOB_214=hisobla(JAMI_214)
        HISOB_215=hisobla(JAMI_215)
        HISOB_216=hisobla(JAMI_216)
        HISOB_218=hisobla(JAMI_218)


        #-------------------------------------------------------------------------------------------------------------
        from functools import reduce

        dfs = [HISOB_210,HISOB_211,HISOB_212,HISOB_213,HISOB_214,HISOB_215,HISOB_216,HISOB_218]

        # Har bir df’da G1 nomini noyob qilish
        for i, df in enumerate(dfs, start=1):
            df.rename(columns={"G1": f"G1_{i}"}, inplace=True)
            if "NAIMUZ" in df.columns:
                df.set_index("NAIMUZ", inplace=True)

        # Join orqali birlashtirish
        yakuniy = reduce(lambda left, right: left.join(right, how="outer"), dfs)

        # 🔥 Eng muhim qadam — tartibni tiklash
        yakuniy = yakuniy.reindex(HISOB_210.index)

        # Yangi ustun qo‘shish
        yakuniy["G_9"] = yakuniy["G1_1"] - yakuniy["G1_7"]

        yakuniy

        colm = ["G1_1","G1_2","G1_3","G1_4","G1_5","G1_6","G1_7","G1_8","G_9"]
        # yakuniy2 = yakuniy[~(yakuniy[colm] == 0).all(axis=1)]
        yakuniy2=yakuniy.replace("0","-")

   



        # fin VILOYAT BOYICHA ==================================================================================================



        KATALOG09=katalog09[["OKPO","ADRES"]]
        BAZA09=baza09[["OKPO","G1","G2","SATR"]]
        KATALOG09["ADRES"] = KATALOG09["ADRES"].str.replace("`", "'", regex=False).str.capitalize().str.strip()


        #-----------------------------------------------------------------------------------------------------------


        # 1️⃣ 102 va 103 satrlarni ajratamiz
        BAZA09_102 = BAZA09[BAZA09["SATR"] == 102]
        BAZA09_103 = BAZA09[BAZA09["SATR"] == 103]
        KATALOG09["ADRES"] = KATALOG09["ADRES"].str.split(",").str[0]
        # 2️⃣ Har ikkalasini KATALOH bilan bog‘laymiz

        #--------------------------------------------------------------------------------------------------------
        JAMI_102 = pd.merge(BAZA09_102, KATALOG09, on="OKPO", how="left")[["ADRES", "G1","G2"]]
        JAMI_103 = pd.merge(BAZA09_103, KATALOG09, on="OKPO", how="left")[["ADRES", "G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format

        jami_102=JAMI_102.groupby("ADRES")[["G1","G2"]].sum()
        jami_102["102"]=jami_102["G1"]-jami_102["G2"]
        hisob_102=jami_102["102"].reset_index()
        hisob_102

        jami_103=JAMI_103.groupby("ADRES")[["G1","G2"]].sum()
        jami_103["102"]=jami_103["G1"]-jami_103["G2"]
        hisob_103=jami_103["102"].reset_index()
        hisob_103
        H=pd.merge(hisob_103,hisob_102,on="ADRES")
        H["102_x"]=H["102_x"]/1000
        H["102_y"]=H["102_y"]/1000
        H["foiz"]=H["102_y"]/H["102_x"]*100
        H

        JAMI_102 = pd.merge(BAZA09_102, KATALOG09, on="OKPO", how="left")[["ADRES", "G2","G1"]]
        JAMI_103 = pd.merge(BAZA09_103, KATALOG09, on="OKPO", how="left")[["ADRES", "G2","G1"]]



        JAMI102_Z = (
            JAMI_102.groupby("ADRES", as_index=False)
                .agg(
                    G2_COUNT_102=("G2", lambda x: (x > 0).sum()),
                    G2_SUM_1000_102=("G2", lambda x: x.sum() / 1000)
                )
        )
        JAMI102_F = (
            JAMI_102.groupby("ADRES", as_index=False)
                .agg(
                    G2_COUNT_102=("G1", lambda x: (x > 0).sum()),
                    G2_SUM_1000_102=("G1", lambda x: x.sum() / 1000)
                )
        )





        JAMI103_Z = (
            JAMI_103.groupby("ADRES", as_index=False)
                .agg(
                    G2_COUNT_103=("G2", lambda x: (x > 0).sum()),
                    G2_SUM_1000_103=("G2", lambda x: x.sum() / 1000)
                )
        )
        JAMI103_F = (
            JAMI_103.groupby("ADRES", as_index=False)
                .agg(
                    G2_COUNT_103=("G1", lambda x: (x > 0).sum()),
                    G2_SUM_1000_103=("G1", lambda x: x.sum() / 1000)
                )
        )


        dfs = [JAMI103_F,JAMI103_Z,JAMI102_F,JAMI102_Z]

        # Har bir df’da G1 ustun nomini noyob qilish
        for i, df in enumerate(dfs, start=1):
            df.rename(columns={"G1": f"G1_{i}"}, inplace=True)

        # Hammasini 'ADRES' bo‘yicha birlashtirish
        yakuniy = reduce(lambda left, right: pd.merge(left, right, on="ADRES", how="outer"), dfs)

        YAKUN=pd.merge(H,yakuniy,on="ADRES")
        YAKUN

        sum_row = pd.DataFrame({
            "ADRES": ["O'zbekiston Respublikasi"],
            "102_x": [YAKUN["102_x"].sum()],
            "102_y": [YAKUN["102_y"].sum()],
            "foiz": [(YAKUN["102_y"].sum() / YAKUN["102_x"].sum()) * 100],
            "G2_COUNT_103_x": [YAKUN["G2_COUNT_103_x"].sum()],
            "G2_SUM_1000_103_x": [YAKUN["G2_SUM_1000_103_x"].sum()],
            "G2_COUNT_103_y": [YAKUN["G2_COUNT_103_y"].sum()],
            "G2_SUM_1000_103_y": [YAKUN["G2_SUM_1000_103_y"].sum()],
            "G2_COUNT_102_x": [YAKUN["G2_COUNT_102_x"].sum()],
            "G2_SUM_1000_102_x": [YAKUN["G2_SUM_1000_102_x"].sum()],
            "G2_COUNT_102_y": [YAKUN["G2_COUNT_102_y"].sum()],
            "G2_SUM_1000_102_y": [YAKUN["G2_SUM_1000_102_y"].sum()]
        })

        # 4️⃣ Barchasini birlashtiramiz
        JAMI_FINAL = pd.concat([sum_row, YAKUN], ignore_index=True)
        JAMI_FINAL

        viloyat_tartib = [
            "O'zbekiston Respublikasi",
            "Qoraqalpog'iston respublikasi",
            "viloyatlar",
            "Andijon viloyati",
            "Buxoro viloyati",
            "Jizzax viloyati",
            "Qashqadaryo viloyati",
            "Navoiy viloyati",
            "Namangan viloyati",
            "Samarqand viloyati",
            "Surxondaryo viloyati",
            "Sirdaryo viloyati",
            "Toshkent viloyati",
            "Farg'ona viloyati",
            "Xorazm viloyati",
            "Toshkent shahri"
        ]


        JAMI_FINAL=JAMI_FINAL.set_index("ADRES")
        JAMI_FINAL=JAMI_FINAL.reindex(viloyat_tartib)
        colm = ["102_x","102_y","foiz","G2_COUNT_103_x","G2_SUM_1000_103_x","G2_COUNT_103_y",
                "G2_SUM_1000_103_y","G2_COUNT_102_x","G2_SUM_1000_102_x","G2_COUNT_102_y","G2_SUM_1000_102_y"]
        # JAMI_FINAL1 = JAMI_FINAL[~(JAMI_FINAL[colm] == 0).all(axis=1)]

        JAMI_FINAL1=JAMI_FINAL.replace("0","-")


        print("✅ ФИН(обл) sheetga yozildi!")

        # FIN VAZIRLIK boyicha ===========================================================================================





        KATALOG09=katalog09[["SOOGU","OKPO"]]
        BAZA09=baza09[["OKPO","G1","G2","SATR"]]

        # BAZA09=BAZA09[BAZA09["SATR"]==102]

        JAMI09=pd.merge(BAZA09,KATALOG09,on="OKPO",how="left")
        JAMI09=JAMI09[["SOOGU","G1","G2"]]
        pd.options.display.float_format = '{:,.1f}'.format

        # 1️⃣ Ma'lumotlarni tayyorlash
        KATALOG09 = katalog09[["SOOGU", "OKPO"]].copy()
        BAZA09 = baza09[["OKPO", "G1", "G2", "SATR"]].copy()

        # 2️⃣ Kodlar formatini to‘g‘rilash
        KATALOG09["SOOGU"] = KATALOG09["SOOGU"].astype(str).str.zfill(5)

        # 3️⃣ Asosiy kodlar ro‘yxati
        asosiy_kodlar = [
            "01014","01024","01074","01094","01104","01124","01144","01164",
            "01354","03504","04043","04403","04413","06184","06213","06224",
            "06264","07254","08114","08524","08654"
        ]
        # === 5. “Айрим вазирлик ва идоралар бўйича” uchun sum ===



        # 4️⃣ Hisoblash funksiyasi
        asosiy_kodlar = [
            "01014","01024","01074","01094","01104","01124","01144","01164","01354"
        ,"03504","04043","04403","04413","06184","06213","06224","06264","07254","08114","08524","08654"

        ]

        # 👉 faqat ayrimlarini ajratamiz
        ayrim_kodlar = ["01144", "04043","01164","06213", "04413", "06184", "07254"]

        def hisobla(df, satr): 
            B = df[df["SATR"] == satr]
            J = pd.merge(B, KATALOG09, on="OKPO", how="left")[["SOOGU", "G1", "G2"]]
            
            # 🔹 Asosiy kodlar bo‘yicha hisoblash
            asosiy = (
                J[J["SOOGU"].isin(asosiy_kodlar)]
                .groupby("SOOGU", as_index=False)
                .agg(
                    COUNT_G1=("G1", lambda x: (x > 0).sum()),
                    SUM_G1=("G1", lambda x: x.sum() / 1000),
                    COUNT_G2=("G2", lambda x: (x > 0).sum()),
                    SUM_G2=("G2", lambda x: x.sum() / 1000)
                )
            )

            # 🔹 Boshqalar (asosiy kodlarga kirmaganlar)
            boshqalar = J[~J["SOOGU"].isin(asosiy_kodlar)]
            boshqalar_agg = pd.DataFrame({
                "SOOGU": ["99999"],
                "COUNT_G1": [(boshqalar["G1"] > 0).sum()],
                "SUM_G1": [boshqalar["G1"].sum() / 1000],
                "COUNT_G2": [(boshqalar["G2"] > 0).sum()],
                "SUM_G2": [boshqalar["G2"].sum() / 1000]
            })

            # 🔹 Jamlangan ro‘yxat
            jami = pd.concat([asosiy, boshqalar_agg], ignore_index=True)

            # 🔹 Ayrim vazirlik va idoralar bo‘yicha (faqat ayrim_kodlar bo‘yicha)
            ayrim = asosiy[asosiy["SOOGU"].isin(ayrim_kodlar)]
            ayrim_sum = pd.DataFrame({
                "SOOGU": ["00001"],
                "COUNT_G1": [ayrim["COUNT_G1"].sum()],
                "SUM_G1": [ayrim["SUM_G1"].sum()],
                "COUNT_G2": [ayrim["COUNT_G2"].sum()],
                "SUM_G2": [ayrim["SUM_G2"].sum()]
            })

            # 🔹 Ўзбекистон Республикаси бўйича жами
            total = pd.DataFrame({
                "SOOGU": ["00000"],
                "COUNT_G1": [jami["COUNT_G1"].sum()],
                "SUM_G1": [jami["SUM_G1"].sum()],
                "COUNT_G2": [jami["COUNT_G2"].sum()],
                "SUM_G2": [jami["SUM_G2"].sum()]
            })

            # 🔹 Hammasini birlashtiramiz
            j = pd.concat([total, ayrim_sum, jami], ignore_index=True)
            
            return j


            
        res102 = hisobla(BAZA09, 102)
        res103 = hisobla(BAZA09, 103)
        res102=res102.fillna(0)
        res103=res103.fillna(0)

        hisob=pd.merge(res103,res102,on="SOOGU")
        hisob["103_zf"]=hisob["SUM_G1_x"]-hisob["SUM_G2_x"]
        hisob["102_zf"]=hisob["SUM_G1_y"]-hisob["SUM_G2_y"]
        hisob

        mapping_list = [
            ["00000", "Республика бўйича жами"],
            ["00001", "Айрим вазирлик ва идоралар бўйича"],
            ["04403", "Ўзбекистон Республикаси Қурилиш ва уй-жой коммунал хўжалиги вазирлиги"],
            ["01354", "«Ўзавтосаноат» АЖ"],
            ["08114", "«Ўздонмаҳсулот» АК"],
            ["08654", "«Ўзкимёсаноат» АЖ"],
            ["06264", "«Ўзагротехсаноатхолдинг» АЖ"],
            ["03504", "«Ўзбекистон темир йўллари» АЖ"],
            ["01024", "«Ўзбекнефтгаз» АЖ"],
            ["01124", "«Ҳудудгазтаъминот» АЖ"],
            ["01104", "«Ўзтрансгаз» АЖ"],
            ["06224", "«Ўзпахтасаноат» АЖ"],
            ["01014", "«Ўзбекистон миллий электр тармоқлари» АЖ"],
            ["01074", "«Ҳудудий электр тармоқлари» АЖ"],
            ["01094", "«Иссиқлик электр станциялари» АЖ"],
            ["08524", "Ўзбекистон Республикаси Тоғ-кон саноати ва геология вазирлиги"],
            
            # ["06213", "«Олмалиқ кон-металлургия комбинати» АЖ"],
            # ["01164", "«Навоий кон-металлургия комбинати» АЖ"],
            ["99999", "Бошқалар"]
        ]
        mapping_df = pd.DataFrame(mapping_list, columns=["SOOGU", "NAIMUZ"])

        # ==============================
        # 7️⃣ Mapping bilan birlashtiramiz
        # ==============================
        hisob = mapping_df.merge(hisob, on="SOOGU", how="left").fillna(0)

        # ==============================
        # 8️⃣ Tartibni mapping_list tartibida saqlaymiz',
        # ==============================
        hisob["order"] = hisob.index
        yakuniy = hisob.sort_values("order").drop(columns="order")
        yakuniy["FOIZ"]=yakuniy["102_zf"]/yakuniy["103_zf"]*100
        yakuniy
        YAKUN2=yakuniy = yakuniy[[
            "NAIMUZ", "103_zf", "102_zf", "FOIZ",
            "COUNT_G1_x", "SUM_G1_x", "COUNT_G2_x", "SUM_G2_x",
            "COUNT_G1_y", "SUM_G1_y", "COUNT_G2_y", "SUM_G2_y"
        ]]

        colm = ["103_zf", "102_zf", "FOIZ",
            "COUNT_G1_x", "SUM_G1_x", "COUNT_G2_x", "SUM_G2_x",
            "COUNT_G1_y", "SUM_G1_y", "COUNT_G2_y", "SUM_G2_y"]
        # JAMI_FINAL1 = JAMI_FINAL1[~(JAMI_FINAL1[colm] == 0).all(axis=1)]

        YAKUN2=YAKUN2.set_index("NAIMUZ")
        YAKUN2=YAKUN2.replace("0","-")

       
        

        yoz_sheetga(df_final,wb,"дебитор-по министр",start_row=10,start_col=2)
        yoz_sheetga(df_final_2,wb,"кредитор-по министр",start_row=9,start_col=2)
        yoz_sheetga(DEB_VILOYAT,wb,"дебитор-по обл",start_row=8,start_col=2)
        yoz_sheetga(KIR_VILOYAT,wb,"кредитор-по обл",start_row=8,start_col=2)
        yoz_sheetga(JAMI_ub,wb,"обл убытка",start_row=5,start_col=2)
        yoz_sheetga(yakuniy_v,wb,"минс убытка",start_row=6,start_col=2)
        yoz_sheetga(YAKUN1,wb,"таб 1",start_row=7,start_col=2)
        yoz_sheetga(YAKUN3,wb,"таб 3",start_row=7,start_col=2)
        yoz_sheetga(yakuniy1,wb,"таб 5",start_row=7,start_col=2)
        yoz_sheetga(yakuniy2,wb,"таб 7",start_row=7,start_col=2)
        yoz_sheetga(JAMI_FINAL1,wb,"ФИН(обл)",start_row=6,start_col=2)
        yoz_sheetga(YAKUN2,wb,"ФИН (мин)",start_row=6,start_col=2)






      
        excel_buffer = BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)

        # 🔹 PDF
        pdf_buffer = excel_bytes_to_pdf_bytes(excel_buffer)

        # 🔽 Yuklab olish
        st.download_button(
            "📥 Excel yuklab olish",
            data=excel_buffer,
            file_name=f"{output_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.download_button(
            "📄 PDF yuklab olish",
            data=pdf_buffer,
            file_name=f"{output_name}.pdf",
            mime="application/pdf"
        )












# cd "C:\Users\hp\Desktop\python\12 MOLIYA.APP"
# streamlit run  app.py 