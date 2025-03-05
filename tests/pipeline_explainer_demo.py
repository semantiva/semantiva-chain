from semantiva_chain.core.workflow_explainer import WorkflowExplainer
from semantiva.logger import Logger
from datetime import datetime

logger = Logger()
logger.set_file_output(
    f"logs/pipeline_explainer_demo{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

workflow_explainer = WorkflowExplainer()

node_configurations = [
    {
        "processor": "TwoDTiltedGaussianFitterProbe",
        # Extract complete fitting parameters from a 2D Gaussian fitter probe.
        # This node isolates parameters (e.g., standard deviation, angle) from the model fitter.
        "context_keyword": "gaussian_fit_parameters",
        # The extracted parameters will be stored in the context under the keyword 'gaussian_fit_parameters'.
    },
    {
        "processor": "ModelFittingContextProcessor",
        "parameters": {
            "fitting_model": "PolynomialFittingModel(degree=1)",
            # Use a linear model to fit the data.
            "independent_var_key": "t_values",
            # The independent variable is taken from the 't_values' in the context.
            "dependent_var_key": (
                "gaussian_fit_parameters",
                "std_dev_x",
            ),
            # Extracts the x-component of the standard deviation from the Gaussian fit parameters.
            "context_keyword": "std_dev_coefficients",
            # The resulting linear fit coefficients for std_dev_x will be saved under 'std_dev_coefficients'.
        },
    },
    {
        "processor": "ModelFittingContextProcessor",
        "parameters": {
            "fitting_model": "PolynomialFittingModel(degree=1)",
            # Use a linear model to fit the orientation feature.
            "independent_var_key": "t_values",
            "dependent_var_key": (
                "gaussian_fit_parameters",
                "angle",
            ),
            # Extracts the orientation angle from the Gaussian fit parameters.
            "context_keyword": "orientation_coefficients",
            # The resulting linear fit coefficients for the angle will be stored under 'orientation_coefficients'.
        },
    },
]

explanation = workflow_explainer.explain(node_configurations)
logger.info(explanation)
