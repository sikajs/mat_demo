專案中利用 Python 結合 pandas 實現了一個具備 可解耦後端架構 的數據分析平台原型，專注於半導體製程原料（如 CVD, Cleaning 製程）的成本核算與 供應鏈風險評估

目標是將基礎物料數據（unit_cost_usd, usage_process, country_of_origin轉化為高階的營運洞察，解決製造業的兩大痛點：

A. 即時製程原料成本核算
- 功能描述： 允許使用者選取特定製程（如 CVD, Cleaning, Etching，並加入對應物料（如 Dicing Tape UV Type, Photoresist AR-450）及數量，即時計算總成本（USD Cost）。

B. 供應鏈韌性與風險分析（國家集中度評估）
- 功能描述： 依據材料的 來源國（country_of_origin）
即時計算該來源國成本佔比（個別項目 USD Cost / 總成本 * 100），並同時以表格和 matplotlib 繪圖 bar chart 呈現結果。

技術特點:
除了可以使用 SQLite3 進行快速開發與試驗，同時也成功實作了可以在 SQLite3 與 PostgreSQL 之間快速切換的模組。
採用抽象化接口（Abstraction Layer）的設計模式，確保上層業務邏輯（成本計算、製程篩選）與底層資料庫實作完全分離。
另外也可以以material_id快速搜尋單一原物料，或是以不同 category 來快速篩選相關原物料。

同時為了專案需要，以 ChatGPT 產生半導體原物料的模擬資料後，專案模擬了從 CSV（半導體物料數據集）到結構化資料庫的資料轉換過程，實務上可以對各個環節進行深化或抽換來實現更強的功能與應對新出現的不同需求

此外專案中也包含以 docker-compose 來執行 專案中需存取的 postgresql database 和 fastapi service


**如何啟動本專案**

使用專案程式前請執行下列指令來啟動 postgresql 資料庫 和 fastapi server

Windows/Mac平台:

1. 安裝並啟動 docker desktop
2. cd docker_env 資料夾
3. 執行 docker-compose up -d
4. 確定有安裝 python3
5. 在專案目錄下執行 pip install -r requirements.txt 來安裝需要的 package
6. 切換到 main.py 用 IDE 執行或是在命令列下執行 python main.py
