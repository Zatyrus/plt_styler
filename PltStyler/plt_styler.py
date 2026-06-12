## Dependiencies
import json
import os
import matplotlib.pyplot as plt
from typing import Dict, Any, List, NoReturn, Union


class PltStyler:
    stylesheet: Dict[str, Any]
    available_stylesheets: list
    verbose: bool

    def __init__(
        self, stylesheet: Union[str, Dict[str, Any]] = None, verbose: bool = False
    ) -> "PltStyler":
        # set verbosity level for debug output
        self.verbose = verbose

        # check available stylesheets in the stylesheets directory
        self.available_stylesheets = self.check_available_stylesheets()

        # check if the provided stylesheet is a string (path to JSON file) or a dictionary, and load it accordingly
        if isinstance(stylesheet, str):
            if stylesheet in self.available_stylesheets:
                # Load the predefined stylesheet
                with open(
                    os.path.join(
                        os.path.dirname(__file__), "stylesheets", f"{stylesheet}.json"
                    ),
                    "r",
                ) as f:
                    self.stylesheet = json.load(f)
            else:
                # Load the custom stylesheet from the provided path
                with open(stylesheet, "r") as f:
                    self.stylesheet = json.load(f)

            if self.verbose:
                print(f"Stylesheet provided as a string, loaded from {stylesheet}.")

        elif isinstance(stylesheet, dict):
            self.stylesheet = stylesheet
            if self.verbose:
                print("Stylesheet provided as a dictionary, using provided settings.")

        else:
            self.stylesheet = {
                "style": "default",
                "font": {"family": "DejaVu Sans", "weight": "bold", "size": 12},
            }

            if self.verbose:
                print("No stylesheet provided, using default settings.")

    # %% Colorbar styling method
    def make_scalar_mappable(
        self, data: Any, cmap: str = "viridis", normalize: bool = True
    ) -> plt.cm.ScalarMappable:
        """Create a scalar mappable for a colorbar based on the provided data and colormap. The scalar mappable can be normalized based on the minimum and maximum values of the data.

        Args:
            data (Any): Iterable data for which the color axis will be created. This can be a list, numpy array, pandas Series, etc.
            cmap (str, optional): The colormap to use. Defaults to "viridis".
            normalize (bool, optional): Whether to normalize the color axis based on the data's minimum and maximum values. Defaults to True.

        Returns:
            plt.cm.ScalarMappable: The scalar mappable for the colorbar.
        """
        norm = plt.Normalize(vmin=data.min(), vmax=data.max()) if normalize else None
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        return sm

    def make_colorbar(
        self,
        data: Any,
        ax: plt.Axes,
        cmap: str = "viridis",
        label: str = "Colorbar",
        fontsize: int = 12,
        fontweight: str = "bold",
    ) -> plt.colorbar:
        """Create a matplotlib colorbar object based on the provided data and colormap, and set the label with the specified font properties.

        Args:
            data (Any): Iterable data for which the colorbar will be created. This can be a list, numpy array, pandas Series, etc.
            cmap (str, optional): The colormap to use. Defaults to "viridis".
            label (str, optional): The label for the colorbar. Defaults to "Colorbar".
            fontsize (int, optional): The font size for the colorbar label. Defaults to 12.
            fontweight (str, optional): The font weight for the colorbar label. Defaults to "bold".

        Returns:
            plt.colorbar: The created colorbar object.
        """
        cbar = plt.colorbar(self.make_scalar_mappable(data, cmap=cmap), ax=ax)
        cbar.set_label(label, fontsize=fontsize, fontweight=fontweight)
        return cbar

    def make_color_and_colorbar(
        self,
        data: Any,
        ax: plt.Axes,
        cmap: str = "viridis",
        label: str = "Colorbar",
        fontsize: int = 12,
        fontweight: str = "bold",
    ) -> tuple[plt.cm.ScalarMappable, plt.colorbar]:
        """Create a scalar mappable and a colorbar object based on the provided data and colormap.

        Args:
            data (Any): Iterable data for which the colorbar will be created.
            ax (plt.Axes): The axes on which to place the colorbar.
            cmap (str, optional): The colormap to use. Defaults to "viridis".
            label (str, optional): The label for the colorbar. Defaults to "Colorbar".
            fontsize (int, optional): The font size for the colorbar label. Defaults to 12.
            fontweight (str, optional): The font weight for the colorbar label. Defaults to "bold".

        Returns:
            tuple[plt.cm.ScalarMappable, plt.colorbar]: The created scalar mappable and colorbar objects.
        """
        sm = self.make_scalar_mappable(data, cmap=cmap)
        cbar = self.make_colorbar(
            data, ax, cmap=cmap, label=label, fontsize=fontsize, fontweight=fontweight
        )
        return sm, cbar

    def make_RGB_array(
        self, data: Any, cmap: str = "viridis", normalize: bool = True
    ) -> Any:
        """Convert the provided data into an RGB array based on the specified colormap and normalization.

        Args:
            data (Any): Iterable data to be converted into an RGB array. This can be a list, numpy array, pandas Series, etc.
            cmap (str, optional): The colormap to use for the conversion. Defaults to "viridis".
            normalize (bool, optional): Whether to normalize the data based on its minimum and maximum values before applying the colormap. Defaults to True.

        Returns:
            Any: An RGB array representing the input data colored according to the specified colormap.
        """
        norm = plt.Normalize(vmin=data.min(), vmax=data.max()) if normalize else None
        cmap_func = plt.cm.get_cmap(cmap)
        rgb_array = cmap_func(norm(data)) if norm else cmap_func(data)
        return rgb_array

    # %% Default parameters for different plot types
    def get_default_parameters(self, plot_type: str) -> Dict[str, Any]:
        """Return the default parameters for a given plot type by loading them from a JSON file in the default_parameters directory.
        The JSON file should be named after the plot type (e.g., lineplot.json for "lineplot") and contain a dictionary of default parameters.

        Args:
            plot_type (str): The type of plot for which to retrieve default parameters.

        Raises:
            ValueError: If no default parameters are found for the specified plot type.

        Returns:
            Dict[str, Any]: The default parameters for the specified plot type.
        """
        default_parameters_dir = os.path.join(
            os.path.dirname(__file__), "default_parameters"
        )
        default_parameters_path = os.path.join(
            default_parameters_dir, f"{plot_type}.json"
        )

        if os.path.exists(default_parameters_path):
            with open(default_parameters_path, "r") as f:
                default_parameters = json.load(f)
            return default_parameters
        else:
            raise ValueError(
                f"No default parameters found for plot type '{plot_type}'."
            )

    # %% Stylesheet management methods
    def reset_style(self) -> NoReturn:
        """Reset the matplotlib style to the default settings.

        Returns:
            NoReturn: This method does not return anything.
        """
        plt.style.use("default")

    def reset_font(self) -> NoReturn:
        """Reset the matplotlib font settings to the default values (family: DejaVu Sans, weight: bold, size: 12).

        Returns:
            NoReturn: This method does not return anything.
        """
        plt.rc("font", family="DejaVu Sans", weight="bold", size=12)

    def check_available_stylesheets(self) -> List[str]:
        """Retrieve a list of available stylesheets by checking the stylesheets directory for JSON files and returning their names without the .json extension.

        Returns:
            List[str]: A list of available stylesheet names.
        """
        stylesheets_dir = os.path.join(os.path.dirname(__file__), "stylesheets")
        available_stylesheets = [
            f[:-5] for f in os.listdir(stylesheets_dir) if f.endswith(".json")
        ]
        return available_stylesheets

    def check_available_default_parameters(self) -> List[str]:
        """Check the available default parameters by looking for JSON files in the default_parameters directory and returning their names without the .json extension.

        Returns:
            List[str]: A list of available default parameter names.
        """
        default_parameters_dir = os.path.join(
            os.path.dirname(__file__), "default_parameters"
        )
        available_default_parameters = [
            f[:-5] for f in os.listdir(default_parameters_dir) if f.endswith(".json")
        ]
        return available_default_parameters

    def reset_stylesheet(self) -> NoReturn:
        """Reset the stylesheet to the default settings by loading the default stylesheet from the stylesheets directory and applying it to matplotlib.

        Returns:
            NoReturn: This method does not return anything.
        """
        # load the default stylesheet from the stylesheets directory
        with open(
            os.path.join(os.path.dirname(__file__), "stylesheets/default.json"),
            "r",
        ) as f:
            self.stylesheet = json.load(f)

        # enforce the default stylesheet
        plt.style.use(self.stylesheet["style"])
        plt.rc("font", **self.stylesheet["font"])

    # %% Methods to set and apply stylesheets and fonts
    def set_font(
        self, family: str = "DejaVu Sans", weight: str = "bold", size: int = 12
    ) -> "PltStyler":
        """Set the font properties in the stylesheet to the specified values for family, weight, and size. This method updates the font settings in the stylesheet dictionary and returns the PltStyler instance for method chaining.

        Args:
            family (str, optional): The font family. Defaults to "DejaVu Sans".
            weight (str, optional): The font weight. Defaults to "bold".
            size (int, optional): The font size. Defaults to 12.

        Returns:
            PltStyler: The PltStyler instance for method chaining.
        """
        self.stylesheet["font"]["family"] = family
        self.stylesheet["font"]["weight"] = weight
        self.stylesheet["font"]["size"] = size

        return self

    def set_style(self, style: str) -> "PltStyler":
        """Set the matplotlib style in the stylesheet to the specified style name. This method updates the style setting in the stylesheet dictionary and returns the PltStyler instance for method chaining.

        Args:
            style (str): The matplotlib style name.

        Returns:
            PltStyler: The PltStyler instance for method chaining.
        """
        self.stylesheet["style"] = style

        return self

    def set_stylesheet(self, stylesheet: Union[str, Dict[str, Any]]) -> "PltStyler":
        """Set the stylesheet for the PltStyler instance by loading it from a specified source.

        Args:
            stylesheet (Union[str, Dict[str, Any]]): The stylesheet to load. This can be a string representing the name of a predefined stylesheet (e.g., "dark", "bright") or a path to a custom JSON file containing the stylesheet settings, or it can be a dictionary with the stylesheet settings.

        Raises:
            ValueError: If the provided stylesheet is not a valid string or dictionary.

        Returns:
            PltStyler: The PltStyler instance with the updated stylesheet for method chaining.
        """
        # check if the provided stylesheet is a string (path to JSON file) or a dictionary, and load it accordingly
        if isinstance(stylesheet, str):
            if stylesheet in self.available_stylesheets:
                # Load the predefined stylesheet
                with open(
                    os.path.join(
                        os.path.dirname(__file__), "stylesheets", f"{stylesheet}.json"
                    ),
                    "r",
                ) as f:
                    self.stylesheet = json.load(f)
            else:
                # Load the custom stylesheet from the provided path
                with open(stylesheet, "r") as f:
                    self.stylesheet = json.load(f)

            if self.verbose:
                print(f"Stylesheet provided as a string, loaded from {stylesheet}.")

        elif isinstance(stylesheet, dict):
            self.stylesheet = stylesheet
            if self.verbose:
                print("Stylesheet provided as a dictionary, using provided settings.")

        else:
            raise ValueError(
                "Stylesheet must be either a string (path to JSON file) or a dictionary."
            )

        return self

    def apply(self) -> NoReturn:
        """Apply the stylesheet (style and font settings) to matplotlib by enforcing both the style and font settings from the stylesheet dictionary.

        Returns:
            NoReturn: This method does not return anything.
        """
        # reset to default to avoid compounding styles when calling this method multiple times
        self.reset_style()
        self.reset_font()

        # enforce the stylesheet
        plt.style.use(self.stylesheet["style"])
        plt.rc("font", **self.stylesheet["font"])
