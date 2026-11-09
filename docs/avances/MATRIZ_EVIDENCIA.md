# Matriz de evidencia técnica

Esta matriz permite defender una afirmación localizando su implementación y una comprobación concreta. La suite completa tuvo 47 casos aprobados el 5 de noviembre de 2026; algunas funciones se parametrizan y ejecutan varios casos. La tabla no sustituye observación institucional, evaluación del modelo ni demostración con hardware real.

| Afirmación verificable | Implementación | Prueba existente | Límite |
|---|---|---|---|
| Una traza válida completa puede reconocerse formalmente | app/automata.py, recognize | tests/test_engine.py::test_formal_recognizer_and_complete_transition_definition | Lenguaje sobre eventos discretos |
| Se completa el ciclo lógico de préstamo y devolución | app/engine.py | tests/test_engine.py::test_ten_complete_cycles | Observaciones controladas, sin cámara |
| Un evento inválido no altera los dos estados | app/engine.py, action | tests/test_engine.py::test_invalid_actions_preserve_both_states | Casos definidos en la suite |
| Un objeto incorrecto no completa la devolución | app/engine.py, _evaluate | tests/test_engine.py::test_wrong_tool_never_closes_return | Etiquetas inyectadas por adaptador de test |
| El cierre necesita imágenes nuevas para verificar | app/engine.py, evidence y _evaluate | tests/test_engine.py::test_post_close_requires_new_frames | El test verifica marcas temporales simuladas |
| Baja confianza no equivale a vacío | app/engine.py | tests/test_engine.py::test_low_confidence_is_not_empty | No estima exactitud de clasificación |
| Cancelar la reserva no crea préstamo | app/engine.py | tests/test_engine.py::test_cancel_does_not_create_loan | Hardware simulado |
| Se controla devolución por titular y revisión por encargado | app/engine.py | tests/test_engine.py::test_only_borrower_can_return_and_only_admin_can_review | Códigos de demostración |
| Se evita duplicación por concurrencia y reenvío | app/engine.py, loans y requests | tests/test_engine.py::test_idempotence_and_simultaneous_requests | Un proceso y SQLite local |
| Un reinicio no completa una devolución pendiente | app/engine.py | tests/test_engine.py::test_restart_does_not_complete_pending_return | Base temporal de prueba |
| El monitor no recibe controles ni token | app/web.py y templates/portal.html | tests/test_web.py::test_monitor_has_no_controls_or_token | Controles de prototipo local |
| Escrituras requieren control local, origen y token | app/web.py | tests/test_web.py::test_local_token_and_same_origin_required | No es auditoría integral de seguridad |
| El historial puede recuperarse y exportarse | app/web.py | tests/test_web.py::test_history_cursor_reconnect_and_csv | Historial de prueba |
| Capturar sin modelo no autoriza préstamos | app/camera.py y app/engine.py | tests/test_camera_dataset.py::test_capture_without_model_does_not_authorize_anything | No demuestra desempeño de un modelo |
| Se rechazan clases faltantes y sesiones compartidas entre conjuntos | tools/train_model.py | tests/test_camera_dataset.py::test_dataset_checker_rejects_missing_classes_and_session_leak | La revisión de calidad visual sigue siendo humana |
| Los cinco escenarios siguen los autómatas compartidos | simulator/engine.py | tests/test_simulator.py::test_all_demonstrations_follow_shared_automata | Simulación independiente |
| La vista de tablet del simulador es de lectura | simulator/web.py | tests/test_simulator.py::test_tablet_only_receives_diagrams_and_cannot_control | Debe validarse además la red física |

Para una revisión posterior, ejecutar la suite y conservar su salida antes de actualizar la fecha o los resultados. Una modificación de los requisitos requiere actualizar la asociación con la prueba o señalar la cobertura pendiente.
