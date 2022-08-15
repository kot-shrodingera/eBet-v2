	def DOM_querySelector(self, nodeId, css_selector):
		"""
		Function path: DOM.querySelector
			Domain: DOM
			Method name: querySelector
		
			Parameters:
				Required arguments:
					'nodeId' (type: NodeId) -> Id of the node to query upon.
					'css_selector' (type: string) -> CSS selector string.
			Returns:
				'nodeId' (type: NodeId) -> Query selector result.
		
			Description: Executes `querySelector` on a given node.
		"""
		assert isinstance(css_selector, (str,)
		    ), "Argument 'css_selector' must be of type '['str']'. Received type: '%s'" % type(
		    css_selector)
		subdom_funcs = self.synchronous_command('DOM.querySelector', nodeId=
		    nodeId, selector=css_selector)
		return subdom_funcs

	def DOM_querySelectorAll(self, nodeId, css_selector):
		"""
		Function path: DOM.querySelectorAll
			Domain: DOM
			Method name: querySelectorAll
		
			Parameters:
				Required arguments:
					'nodeId' (type: NodeId) -> Id of the node to query upon.
					'css_selector' (type: string) -> CSS selector string.
			Returns:
				'nodeIds' (type: array) -> Query selector result.
		
			Description: Executes `querySelectorAll` on a given node.
		"""
		assert isinstance(css_selector, (str,)
		    ), "Argument 'css_selector' must be of type '['str']'. Received type: '%s'" % type(
		    css_selector)
		subdom_funcs = self.synchronous_command('DOM.querySelectorAll', nodeId=
		    nodeId, selector=css_selector)
		return subdom_funcs


	def Runtime_evaluate(self, expression, **kwargs):
		"""
		Function path: Runtime.evaluate
			Domain: Runtime
			Method name: evaluate
		
			Parameters:
				Required arguments:
					'expression' (type: string) -> Expression to evaluate.
				Optional arguments:
					'objectGroup' (type: string) -> Symbolic group name that can be used to release multiple objects.
					'includeCommandLineAPI' (type: boolean) -> Determines whether Command Line API should be available during the evaluation.
					'silent' (type: boolean) -> In silent mode exceptions thrown during evaluation are not reported and do not pause
execution. Overrides `setPauseOnException` state.
					'contextId' (type: ExecutionContextId) -> Specifies in which execution context to perform evaluation. If the parameter is omitted the
evaluation will be performed in the context of the inspected page.
This is mutually exclusive with `uniqueContextId`, which offers an
alternative way to identify the execution context that is more reliable
in a multi-process environment.
					'returnByValue' (type: boolean) -> Whether the result is expected to be a JSON object that should be sent by value.
					'generatePreview' (type: boolean) -> Whether preview should be generated for the result.
					'userGesture' (type: boolean) -> Whether execution should be treated as initiated by user in the UI.
					'awaitPromise' (type: boolean) -> Whether execution should `await` for resulting value and return once awaited promise is
resolved.
					'throwOnSideEffect' (type: boolean) -> Whether to throw an exception if side effect cannot be ruled out during evaluation.
This implies `disableBreaks` below.
					'timeout' (type: TimeDelta) -> Terminate execution after timing out (number of milliseconds).
					'disableBreaks' (type: boolean) -> Disable breakpoints during execution.
					'replMode' (type: boolean) -> Setting this flag to true enables `let` re-declaration and top-level `await`.
Note that `let` variables can only be re-declared if they originate from
`replMode` themselves.
					'allowUnsafeEvalBlockedByCSP' (type: boolean) -> The Content Security Policy (CSP) for the target might block 'unsafe-eval'
which includes eval(), Function(), setTimeout() and setInterval()
when called with non-callable arguments. This flag bypasses CSP for this
evaluation and allows unsafe-eval. Defaults to true.
					'uniqueContextId' (type: string) -> An alternative way to specify the execution context to evaluate in.
Compared to contextId that may be reused accross processes, this is guaranteed to be
system-unique, so it can be used to prevent accidental evaluation of the expression
in context different than intended (e.g. as a result of navigation accross process
boundaries).
This is mutually exclusive with `contextId`.
			Returns:
				'result' (type: RemoteObject) -> Evaluation result.
				'exceptionDetails' (type: ExceptionDetails) -> Exception details.
		
			Description: Evaluates expression on global object.
		"""
		assert isinstance(expression, (str,)
		    ), "Argument 'expression' must be of type '['str']'. Received type: '%s'" % type(
		    expression)
		if 'objectGroup' in kwargs:
			assert isinstance(kwargs['objectGroup'], (str,)
			    ), "Optional argument 'objectGroup' must be of type '['str']'. Received type: '%s'" % type(
			    kwargs['objectGroup'])
		if 'includeCommandLineAPI' in kwargs:
			assert isinstance(kwargs['includeCommandLineAPI'], (bool,)
			    ), "Optional argument 'includeCommandLineAPI' must be of type '['bool']'. Received type: '%s'" % type(
			    kwargs['includeCommandLineAPI'])
		if 'silent' in kwargs:
			assert isinstance(kwargs['silent'], (bool,)
			    ), "Optional argument 'silent' must be of type '['bool']'. Received type: '%s'" % type(
			    kwargs['silent'])
		if 'contextId' in kwargs:
			assert isinstance(kwargs['contextId'], (int,)
			    ), "Optional argument 'contextId' must be of type '['str']'. Received type: '%s'" % type(
			    kwargs['contextId'])