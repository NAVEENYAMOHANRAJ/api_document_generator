"""
Semantic resolver for determining endpoint meaning from controller actions and HTTP methods.

This module resolves the true semantic meaning of endpoints by analyzing:
1. Controller action names (index, show, store, create, update, destroy, etc.)
2. Framework conventions (Laravel, Django, Rails, etc.)
3. HTTP method semantics
4. Response types and patterns

This prevents naive HTTP-method-only summaries like "Create jobs" for POST /jobs
when the actual handler is QueueController@index (which should be "List jobs").
"""

from typing import Optional, Dict, Tuple


class SemanticResolver:
    """Resolve endpoint semantics from controller actions and HTTP methods."""

    # Standard REST action semantics across frameworks
    ACTION_SEMANTICS = {
        # List/Retrieve operations
        "index": "List",
        "list": "List",
        "all": "List",
        "get_all": "List",
        "fetch": "Fetch",
        "fetch_all": "Fetch all",
        "retrieve": "Retrieve",
        "retrieve_all": "Retrieve all",
        "search": "Search",
        "query": "Query",
        "find": "Find",
        "find_all": "Find all",
        "get": "Get",
        "read": "Read",
        "show": "Retrieve",
        "view": "View",
        "display": "Display",
        "details": "Get details",
        "info": "Get info",
        "get_info": "Get info",
        
        # Create operations
        "store": "Create",
        "create": "Create",
        "add": "Add",
        "insert": "Insert",
        "new": "Create new",
        "post": "Create",
        "save": "Save",
        "register": "Register",
        "signup": "Sign up",
        "enroll": "Enroll",
        "subscribe": "Subscribe",
        
        # Update operations
        "update": "Update",
        "edit": "Update",
        "modify": "Modify",
        "patch": "Update",
        "put": "Replace",
        "change": "Change",
        "set": "Set",
        "refresh": "Refresh",
        "sync": "Sync",
        "toggle": "Toggle",
        "enable": "Enable",
        "disable": "Disable",
        "activate": "Activate",
        "deactivate": "Deactivate",
        "publish": "Publish",
        "unpublish": "Unpublish",
        "archive": "Archive",
        "restore": "Restore",
        
        # Delete operations
        "destroy": "Delete",
        "delete": "Delete",
        "remove": "Remove",
        "drop": "Drop",
        "purge": "Purge",
        "clear": "Clear",
        "truncate": "Truncate",
        "erase": "Erase",
        "unsubscribe": "Unsubscribe",
        "logout": "Logout",
        
        # Authentication operations
        "login": "Authenticate",
        "authenticate": "Authenticate",
        "auth": "Authenticate",
        "signin": "Sign in",
        "logout": "Logout",
        "signout": "Sign out",
        "verify": "Verify",
        "validate": "Validate",
        "confirm": "Confirm",
        "reset": "Reset",
        "refresh_token": "Refresh token",
        
        # Bulk operations
        "bulk_create": "Bulk create",
        "bulk_update": "Bulk update",
        "bulk_delete": "Bulk delete",
        "batch_create": "Batch create",
        "batch_update": "Batch update",
        "batch_delete": "Batch delete",
        "import": "Import",
        "export": "Export",
        
        # Status/State operations
        "status": "Get status",
        "health": "Health check",
        "ping": "Ping",
        "check": "Check",
        "validate_token": "Validate token",
        "check_availability": "Check availability",
        
        # Relationship operations
        "attach": "Attach",
        "detach": "Detach",
        "sync_relations": "Sync relations",
        "associate": "Associate",
        "dissociate": "Dissociate",
        
        # Count/Statistics operations
        "count": "Count",
        "stats": "Get statistics",
        "statistics": "Get statistics",
        "summary": "Get summary",
        "aggregate": "Aggregate",
        
        # Export/Download operations
        "download": "Download",
        "export_csv": "Export as CSV",
        "export_pdf": "Export as PDF",
        "generate_report": "Generate report",
        
        # Upload operations
        "upload": "Upload",
        "import_file": "Import file",
        "process_file": "Process file",
    }

    # HTTP method to semantic action mapping (fallback when action is unknown)
    HTTP_METHOD_SEMANTICS = {
        "GET": "Retrieve",
        "POST": "Create",
        "PUT": "Replace",
        "PATCH": "Update",
        "DELETE": "Delete",
        "HEAD": "Inspect",
        "OPTIONS": "Describe",
    }

    # Framework-specific conventions
    FRAMEWORK_CONVENTIONS = {
        "laravel": {
            "index": ("GET", "List"),
            "create": ("GET", "Show create form"),
            "store": ("POST", "Create"),
            "show": ("GET", "Retrieve"),
            "edit": ("GET", "Show edit form"),
            "update": ("PUT", "Update"),
            "destroy": ("DELETE", "Delete"),
        },
        "django": {
            "list": ("GET", "List"),
            "create": ("POST", "Create"),
            "retrieve": ("GET", "Retrieve"),
            "update": ("PUT", "Update"),
            "partial_update": ("PATCH", "Update"),
            "destroy": ("DELETE", "Delete"),
        },
        "rails": {
            "index": ("GET", "List"),
            "new": ("GET", "Show new form"),
            "create": ("POST", "Create"),
            "show": ("GET", "Retrieve"),
            "edit": ("GET", "Show edit form"),
            "update": ("PUT", "Update"),
            "destroy": ("DELETE", "Delete"),
        },
        "fastapi": {
            "list": ("GET", "List"),
            "create": ("POST", "Create"),
            "get": ("GET", "Retrieve"),
            "update": ("PUT", "Update"),
            "delete": ("DELETE", "Delete"),
        },
        "express": {
            "list": ("GET", "List"),
            "create": ("POST", "Create"),
            "get": ("GET", "Retrieve"),
            "update": ("PUT", "Update"),
            "delete": ("DELETE", "Delete"),
        },
    }

    @classmethod
    def resolve_semantic_action(
        cls,
        method: str,
        path: str,
        function_name: Optional[str] = None,
        framework: Optional[str] = None,
    ) -> str:
        """
        Resolve the semantic action for an endpoint.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE, etc.)
            path: URL path
            function_name: Controller action name (e.g., "QueueController@index")
            framework: Framework name (e.g., "Laravel", "Django", "FastAPI")

        Returns:
            Semantic action string (e.g., "List", "Create", "Update", "Delete")
        """
        # Extract action name from function_name
        action_name = cls._extract_action_name(function_name)

        # Try action semantics mapping first (most reliable)
        if action_name:
            action_lower = action_name.lower()
            if action_lower in cls.ACTION_SEMANTICS:
                return cls.ACTION_SEMANTICS[action_lower]

        # Try framework-specific convention as secondary check
        if framework and action_name:
            framework_lower = framework.lower()
            if framework_lower in cls.FRAMEWORK_CONVENTIONS:
                conventions = cls.FRAMEWORK_CONVENTIONS[framework_lower]
                if action_name in conventions:
                    expected_method, semantic = conventions[action_name]
                    # Use the semantic from convention
                    return semantic

        # Fallback to HTTP method semantics
        return cls.HTTP_METHOD_SEMANTICS.get(method.upper(), "Call")

    @classmethod
    def resolve_semantic_summary(
        cls,
        method: str,
        path: str,
        resource: str,
        function_name: Optional[str] = None,
        framework: Optional[str] = None,
    ) -> str:
        """
        Generate a semantic summary for an endpoint.

        Args:
            method: HTTP method
            path: URL path
            resource: Resource name extracted from path
            function_name: Controller action name
            framework: Framework name

        Returns:
            Semantic summary (e.g., "List jobs", "Create user", "Delete post")
        """
        action = cls.resolve_semantic_action(method, path, function_name, framework)
        return f"{action} {resource}" if resource else action

    @classmethod
    def _extract_action_name(cls, function_name: Optional[str]) -> Optional[str]:
        """
        Extract action name from function_name.

        Examples:
            "QueueController@index" → "index"
            "UserController@store" → "store"
            "JobViewSet.list" → "list"
            "JobsController#index" → "index"
            "list_jobs" → "list"
            "get_user_by_id" → "get"
        """
        if not function_name:
            return None

        # Handle Laravel-style "Controller@action"
        if "@" in function_name:
            parts = function_name.split("@")
            if len(parts) == 2:
                return parts[1]

        # Handle Rails-style "Controller#action"
        if "#" in function_name:
            parts = function_name.split("#")
            if len(parts) == 2:
                return parts[1]

        # Handle method-style "method_name" or "Class::method"
        if "::" in function_name:
            parts = function_name.split("::")
            if len(parts) == 2:
                return parts[1]

        # Handle dot notation "Class.method" (Django, Python style)
        if "." in function_name:
            parts = function_name.split(".")
            if len(parts) >= 2:
                return parts[-1]

        # Handle underscore-separated names like "list_jobs" or "get_user_by_id"
        # Extract the first meaningful verb
        if "_" in function_name:
            parts = function_name.split("_")
            # Return the first part if it's a known action
            if parts[0].lower() in cls.ACTION_SEMANTICS:
                return parts[0]
            # Otherwise return the whole thing
            return function_name

        # Return as-is if it looks like an action name
        return function_name

    @classmethod
    def is_list_operation(
        cls,
        method: str,
        path: str,
        function_name: Optional[str] = None,
        framework: Optional[str] = None,
    ) -> bool:
        """Check if endpoint is a list/fetch operation."""
        action = cls.resolve_semantic_action(method, path, function_name, framework)
        return action in {"List", "Fetch", "Fetch all", "Retrieve all", "Find all", "Search", "Query"}

    @classmethod
    def is_create_operation(
        cls,
        method: str,
        path: str,
        function_name: Optional[str] = None,
        framework: Optional[str] = None,
    ) -> bool:
        """Check if endpoint is a create operation."""
        action = cls.resolve_semantic_action(method, path, function_name, framework)
        return action in {"Create", "Add", "Insert", "Register", "Sign up", "Enroll", "Subscribe", "Save"}

    @classmethod
    def is_update_operation(
        cls,
        method: str,
        path: str,
        function_name: Optional[str] = None,
        framework: Optional[str] = None,
    ) -> bool:
        """Check if endpoint is an update operation."""
        action = cls.resolve_semantic_action(method, path, function_name, framework)
        return action in {"Update", "Modify", "Replace", "Change", "Set", "Refresh", "Sync", "Toggle"}

    @classmethod
    def is_delete_operation(
        cls,
        method: str,
        path: str,
        function_name: Optional[str] = None,
        framework: Optional[str] = None,
    ) -> bool:
        """Check if endpoint is a delete operation."""
        action = cls.resolve_semantic_action(method, path, function_name, framework)
        return action in {"Delete", "Remove", "Drop", "Purge", "Clear", "Truncate", "Erase"}

    @classmethod
    def is_auth_operation(
        cls,
        method: str,
        path: str,
        function_name: Optional[str] = None,
        framework: Optional[str] = None,
    ) -> bool:
        """Check if endpoint is an authentication operation."""
        action = cls.resolve_semantic_action(method, path, function_name, framework)
        return action in {"Authenticate", "Sign in", "Logout", "Sign out", "Verify", "Validate", "Confirm", "Reset"}
