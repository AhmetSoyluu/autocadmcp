from autocad_mcp_server.tools.common import success_response


def test_generation_tool_response_shape() -> None:
    payload = {
        'workspace': 'C:/workspaces/blueprint-1',
        'lsp_path': 'C:/workspaces/blueprint-1/test.lsp',
        'scr_path': 'C:/workspaces/blueprint-1/test.scr',
        'generated_files': ['a.lsp', 'a.scr'],
    }
    response = success_response('generate_electrical_blueprint', 'generation', payload)
    assert response['ok'] is True
    assert response['tool_name'] == 'generate_electrical_blueprint'
    assert response['payload']['lsp_path'].endswith('.lsp')
    assert response['payload']['scr_path'].endswith('.scr')


def test_generation_tool_response_contains_workspace_metadata() -> None:
    payload = {
        'workspace': 'C:/workspaces/blueprint-2',
        'lsp_path': 'C:/workspaces/blueprint-2/universal.lsp',
        'scr_path': 'C:/workspaces/blueprint-2/universal.scr',
        'generated_files': ['universal.lsp', 'universal.scr'],
        'preview_summary': {'discipline': 'architecture'},
    }
    response = success_response('generate_electrical_blueprint', 'generation', payload)
    assert response['payload']['workspace'].endswith('blueprint-2')
    assert response['payload']['preview_summary']['discipline'] == 'architecture'
