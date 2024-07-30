from pastastore.extensions.accessor import (
    register_pastastore_accessor as register_pastastore_accessor,
)


def activate_hydropandas_extension():
    """Register Plotly extension for pastas.Model class for interactive plotting."""
    from pastastore.extensions.hpd import HydroPandasExtension as HpdExt

    print(
        "Registered HydroPandas extension in PastaStore class, "
        "e.g. `pstore.hpd.download_bro()`."
    )
