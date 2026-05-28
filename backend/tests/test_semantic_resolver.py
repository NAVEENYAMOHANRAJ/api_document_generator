"""
Tests for semantic resolver to ensure correct endpoint meaning extraction.

This test suite validates that the semantic resolver correctly determines
endpoint meanings from controller actions, not just HTTP methods.

Example: POST /jobs with QueueController@index should be "List jobs", not "Create jobs"
"""

import pytest
from api_doc_generator.utils.semantic_resolver import SemanticResolver


class TestSemanticResolver:
    """Test semantic resolution of endpoint meanings."""

    def test_laravel_index_action_is_list(self):
        """Laravel @index action should resolve to List, not Create."""
        action = SemanticResolver.resolve_semantic_action(
            method="GET",
            path="/jobs",
            function_name="QueueController@index",
            framework="Laravel",
        )
        assert action == "List", f"Expected 'List' but got '{action}'"

    def test_laravel_store_action_is_create(self):
        """Laravel @store action should resolve to Create."""
        action = SemanticResolver.resolve_semantic_action(
            method="POST",
            path="/jobs",
            function_name="QueueController@store",
            framework="Laravel",
        )
        assert action == "Create"

    def test_laravel_show_action_is_retrieve(self):
        """Laravel @show action should resolve to Retrieve."""
        action = SemanticResolver.resolve_semantic_action(
            method="GET",
            path="/jobs/{id}",
            function_name="QueueController@show",
            framework="Laravel",
        )
        assert action == "Retrieve"

    def test_laravel_update_action_is_update(self):
        """Laravel @update action should resolve to Update."""
        action = SemanticResolver.resolve_semantic_action(
            method="PUT",
            path="/jobs/{id}",
            function_name="QueueController@update",
            framework="Laravel",
        )
        assert action == "Update"

    def test_laravel_destroy_action_is_delete(self):
        """Laravel @destroy action should resolve to Delete."""
        action = SemanticResolver.resolve_semantic_action(
            method="DELETE",
            path="/jobs/{id}",
            function_name="QueueController@destroy",
            framework="Laravel",
        )
        assert action == "Delete"

    def test_django_list_action_is_list(self):
        """Django list action should resolve to List."""
        action = SemanticResolver.resolve_semantic_action(
            method="GET",
            path="/api/jobs/",
            function_name="JobViewSet.list",
            framework="Django",
        )
        assert action == "List"

    def test_django_create_action_is_create(self):
        """Django create action should resolve to Create."""
        action = SemanticResolver.resolve_semantic_action(
            method="POST",
            path="/api/jobs/",
            function_name="JobViewSet.create",
            framework="Django",
        )
        assert action == "Create"

    def test_fastapi_list_action_is_list(self):
        """FastAPI list action should resolve to List."""
        action = SemanticResolver.resolve_semantic_action(
            method="GET",
            path="/jobs",
            function_name="list_jobs",
            framework="FastAPI",
        )
        assert action == "List"

    def test_semantic_summary_generation(self):
        """Test semantic summary generation with resource name."""
        summary = SemanticResolver.resolve_semantic_summary(
            method="GET",
            path="/jobs",
            resource="jobs",
            function_name="QueueController@index",
            framework="Laravel",
        )
        assert summary == "List jobs"

    def test_semantic_summary_with_create(self):
        """Test semantic summary for create operation."""
        summary = SemanticResolver.resolve_semantic_summary(
            method="POST",
            path="/jobs",
            resource="jobs",
            function_name="QueueController@store",
            framework="Laravel",
        )
        assert summary == "Create jobs"

    def test_semantic_summary_with_update(self):
        """Test semantic summary for update operation."""
        summary = SemanticResolver.resolve_semantic_summary(
            method="PUT",
            path="/jobs/{id}",
            resource="jobs",
            function_name="QueueController@update",
            framework="Laravel",
        )
        assert summary == "Update jobs"

    def test_semantic_summary_with_delete(self):
        """Test semantic summary for delete operation."""
        summary = SemanticResolver.resolve_semantic_summary(
            method="DELETE",
            path="/jobs/{id}",
            resource="jobs",
            function_name="QueueController@destroy",
            framework="Laravel",
        )
        assert summary == "Delete jobs"

    def test_fallback_to_http_method_when_no_action(self):
        """When no function_name provided, fallback to HTTP method semantics."""
        action = SemanticResolver.resolve_semantic_action(
            method="POST",
            path="/jobs",
            function_name=None,
            framework=None,
        )
        assert action == "Create"

    def test_fallback_to_http_method_for_unknown_action(self):
        """When action name is unknown, fallback to HTTP method semantics."""
        action = SemanticResolver.resolve_semantic_action(
            method="POST",
            path="/jobs",
            function_name="QueueController@unknown_action",
            framework="Laravel",
        )
        assert action == "Create"

    def test_extract_action_from_laravel_style(self):
        """Extract action name from Laravel-style Controller@action."""
        action = SemanticResolver._extract_action_name("QueueController@index")
        assert action == "index"

    def test_extract_action_from_method_style(self):
        """Extract action name from method-style Class::method."""
        action = SemanticResolver._extract_action_name("JobService::list")
        assert action == "list"

    def test_is_list_operation(self):
        """Test list operation detection."""
        assert SemanticResolver.is_list_operation(
            method="GET",
            path="/jobs",
            function_name="QueueController@index",
            framework="Laravel",
        )

    def test_is_create_operation(self):
        """Test create operation detection."""
        assert SemanticResolver.is_create_operation(
            method="POST",
            path="/jobs",
            function_name="QueueController@store",
            framework="Laravel",
        )

    def test_is_update_operation(self):
        """Test update operation detection."""
        assert SemanticResolver.is_update_operation(
            method="PUT",
            path="/jobs/{id}",
            function_name="QueueController@update",
            framework="Laravel",
        )

    def test_is_delete_operation(self):
        """Test delete operation detection."""
        assert SemanticResolver.is_delete_operation(
            method="DELETE",
            path="/jobs/{id}",
            function_name="QueueController@destroy",
            framework="Laravel",
        )

    def test_is_auth_operation(self):
        """Test authentication operation detection."""
        assert SemanticResolver.is_auth_operation(
            method="POST",
            path="/login",
            function_name="AuthController@login",
            framework="Laravel",
        )

    def test_critical_issue_post_index_is_list_not_create(self):
        """
        CRITICAL TEST: POST /telescope/telescope-api/jobs with QueueController@index
        should be "List jobs", NOT "Create jobs".

        This was the major architectural weakness that needed fixing.
        """
        summary = SemanticResolver.resolve_semantic_summary(
            method="POST",
            path="/telescope/telescope-api/jobs",
            resource="jobs",
            function_name="QueueController@index",
            framework="Laravel",
        )
        # The action should be "List" from the @index action, not "Create" from POST method
        assert summary == "List jobs", (
            f"CRITICAL: Expected 'List jobs' but got '{summary}'. "
            "The semantic resolver must use controller action, not just HTTP method."
        )

    def test_multiple_framework_conventions(self):
        """Test that different frameworks have correct conventions."""
        # Laravel: GET /jobs -> index -> List
        laravel_action = SemanticResolver.resolve_semantic_action(
            method="GET",
            path="/jobs",
            function_name="JobController@index",
            framework="Laravel",
        )
        assert laravel_action == "List"

        # Django: GET /jobs/ -> list -> List
        django_action = SemanticResolver.resolve_semantic_action(
            method="GET",
            path="/jobs/",
            function_name="JobViewSet.list",
            framework="Django",
        )
        assert django_action == "List"

        # Rails: GET /jobs -> index -> List
        rails_action = SemanticResolver.resolve_semantic_action(
            method="GET",
            path="/jobs",
            function_name="JobsController#index",
            framework="Rails",
        )
        assert rails_action == "List"

    def test_action_semantics_coverage(self):
        """Test that common action names are covered."""
        test_cases = [
            ("index", "List"),
            ("show", "Retrieve"),
            ("store", "Create"),
            ("update", "Update"),
            ("destroy", "Delete"),
            ("create", "Create"),
            ("edit", "Update"),
            ("login", "Authenticate"),
            ("logout", "Logout"),
            ("register", "Register"),
            ("search", "Search"),
            ("export", "Export"),
            ("import", "Import"),
        ]

        for action_name, expected_semantic in test_cases:
            semantic = SemanticResolver.resolve_semantic_action(
                method="GET",
                path="/test",
                function_name=f"TestController@{action_name}",
                framework="Laravel",
            )
            assert semantic == expected_semantic, (
                f"Action '{action_name}' should resolve to '{expected_semantic}' "
                f"but got '{semantic}'"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
