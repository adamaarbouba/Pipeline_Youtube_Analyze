# Clean Project Tree

```text
Pipeline_Youtube_Analyze/
├── .env.example
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── docker-compose.yaml
├── requirements.txt
├── config/
├── dags/
│   └── youtube_pipeline.py
├── data/
│   ├── raw/
│   └── processed/
├── docker/
│   └── postgres/
│       ├── create-elt-tables.sql
│       └── init-multiple-databases.sh
├── include/
├── logs/
├── plugins/
├── scripts/
│   ├── commands.txt
│   └── test_pipeline.sh
├── src/
│   ├── extract_youtube.py
│   ├── extract_video_details.py
│   ├── merge_raw.py
│   ├── load_staging.py
│   └── load_core.py
├── tests/
└── docs/
    ├── README.md
    ├── PROJECT_TREE.md
    ├── cleanup.md
    ├── phases/
    ├── dags/
    ├── src/
    ├── docker/postgres/
    ├── scripts/
    └── data/
```
