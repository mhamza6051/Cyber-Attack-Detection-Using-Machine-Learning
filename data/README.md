# Dataset — CICIDS2017 (not stored in Git)

The raw dataset (~885 MB total) is **not** included in this repository: several files exceed GitHub's 100 MB per-file limit (Monday ≈ 177 MB, Wednesday ≈ 225 MB uncompressed).

## Official source

**CICIDS2017 — Canadian Institute for Cybersecurity, University of New Brunswick**
https://www.unb.ca/cic/datasets/ids-2017.html

Download the "MachineLearningCSV" files and place them in this `data/` folder with these names (as used by the notebook):

- `Monday-WorkingHours.pcap_ISCX.csv`
- `Tuesday-WorkingHours.pcap_ISCX.csv`
- `Wednesday-workingHours.pcap_ISCX.csv`
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`
- `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv`
- `Friday-WorkingHours-Morning.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`

The trained model in `models/` works with the Streamlit app without the dataset — the CSVs are only needed to re-run the training notebook.
