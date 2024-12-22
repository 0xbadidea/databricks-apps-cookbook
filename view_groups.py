groups = [
    {
        "views": [
            {"label": "Book Intro", "page": "views/book_intro.py", "icon": ":material/skillet_cooktop:"},
        ],
    },
    {
        "title": "Tables",
        "views": [
            {"label": "Read a Table", "page": "views/tables_read.py", "icon": ":material/table_view:"},
            {"label": "Edit a Table", "page": "views/tables_edit.py", "icon": ":material/edit_document:"},
        ],
    },
    {
        "title": "Volumes",
        "views": [
            {"label": "Upload a File", "page": "views/volumes_upload.py", "icon": ":material/publish:"},
            {"label": "Download a File", "page": "views/volumes_download.py", "icon": ":material/download:"},
        ],
    },
    {
        "title": "Machine Learning",
        "views": [
            {"label": "Invoke a Model", "page": "views/ml_serving_invoke.py", "icon": ":material/experiment:"},
            {"label": "Call Vector Search", "page": "views/ml_vector_search.py", "icon": ":material/search:"},
        ],
    },
    {
        "title": "Workflows",
        "views": [
            {"label": "Trigger a Pipeline", "page": "views/pipelines_trigger.py", "icon": ":material/valve:"},
            {"label": "Trigger a Job", "page": "views/workflows_trigger.py", "icon": ":material/valve:"},
            {"label": "Get Job Results", "page": "views/workflows_get_results.py", "icon": ":material/account_tree:"},
        ],
    },
    {
        "title": "Users",
        "views": [
            {"label": "Get Current User", "page": "views/users_get_current.py", "icon": ":material/fingerprint:"},
        ],
    },
    {
        "title": "Compute",
        "views": [
            {"label": "Connect", "page": "views/compute_connect.py", "icon": ":material/lan:"},
        ],
    },
]
