groups = [
    {
        "views": [
            {"label": "Book Intro", "help": "", "page": "views/book_intro.py", "icon": ":material/skillet_cooktop:"},
        ],
    },
    {
        "title": "Tables",
        "views": [
            {"label": "Read a Table", "help": "Query a Catalog Delta table.", "page": "views/tables_read.py", "icon": ":material/table_view:"},
            {"label": "Edit a Table", "help": "Interactively edit a Delta table in the UI.", "page": "views/tables_edit.py", "icon": ":material/edit_document:"},
        ],
    },
    {
        "title": "Volumes",
        "views": [
            {"label": "Upload a File", "help": "Upload a file into a Unity Catalog Volume.", "page": "views/volumes_upload.py", "icon": ":material/publish:"},
            {"label": "Download a File", "help": "Download a Volume file.", "page": "views/volumes_download.py", "icon": ":material/download:"},
        ],
    },
    {
        "title": "Machine Learning",
        "views": [
            {"label": "Invoke a Model", "help": "Invoke a model across classical ML and Large Language with UI inputs.", "page": "views/ml_serving_invoke.py", "icon": ":material/experiment:"},
            {"label": "Call Vector Search", "help": "Use Mosaic AI to generate embeddings for textual data and perform vector search.", "page": "views/ml_vector_search.py", "icon": ":material/search:"},
        ],
    },
    {
        "title": "Workflows",
        "views": [
            {"label": "Run a Pipeline", "help": "Run a Delta Live Tables (DLT) Pipeline with UI inputs.", "page": "views/pipelines_run.py", "icon": ":material/valve:"},
            {"label": "Run a Job", "help": "Run a Workflow with UI inputs.", "page": "views/workflows_run.py", "icon": ":material/valve:"},
            {"label": "Get Job Results", "help": "Retrieve results for a Workflow Job run.", "page": "views/workflows_get_results.py", "icon": ":material/account_tree:"},
        ],
    },
    {
        "title": "Compute",
        "views": [
            {"label": "Connect", "help": "Transform data at scale with UI inputs.", "page": "views/compute_connect.py", "icon": ":material/lan:"},
        ],
    },
    {
        "title": "Users",
        "views": [
            {"label": "Get Current User", "help": "Get current App user information.", "page": "views/users_get_current.py", "icon": ":material/fingerprint:"},
        ],
    },
]
