import os
import datetime
from irekua_collections import Collection
from irekua_collections import dataclasses as dt
from irekua_collections.dataclasses import geometry as geom


models = [
    dt.Term,
    dt.Item,
    dt.UserAnnotation,
    dt.Prediction,
    dt.Deployment,
    dt.Device,
    dt.Site,
    dt.SamplingEvent,
    dt.Organism,
    dt.OrganismCapture,
]


def test_collection_context():
    col = Collection()

    with col:
        family = dt.Term(value="Family 1", term_type="Family")
        species = dt.Term(
            value="Species 1",
            term_type="Species",
            parent_id=family.id,
        )
        assert species.parent == family

        supersite = dt.Site(
            geometry=geom.Polygon(
                exterior=[
                    geom.Point(-1, -1),
                    geom.Point(-1, 1),
                    geom.Point(1, 1),
                    geom.Point(1, -1),
                ]
            ),
        )
        site = dt.Site(
            geometry=geom.Point(x=0, y=0),
            parent_id=supersite.id,
        )
        assert site.parent == supersite

        device = dt.Device(device_type="Recorder", model="Audiomoth")
        trap = dt.Device(device_type="Bat Trap")

        super_sampling_event = dt.SamplingEvent(
            site_id=supersite.id,
            started_on=datetime.datetime.now() - datetime.timedelta(days=30),
            ended_on=datetime.datetime.now(),
        )
        assert super_sampling_event.site == supersite

        sampling_event = dt.SamplingEvent(
            site_id=site.id,
            started_on=datetime.datetime.now() - datetime.timedelta(days=30),
            ended_on=datetime.datetime.now(),
            parent_id=super_sampling_event.id,
        )
        assert sampling_event.site == site
        assert sampling_event.parent == super_sampling_event

        organism = dt.Organism(
            name="bat 1",
            organism_type="bat",
            labels=[
                species,
                family,
            ],
        )

        trap_deployment = dt.Deployment(
            sampling_event_id=sampling_event.id,
            deployed_on=sampling_event.started_on,
            recovered_on=sampling_event.ended_on,
            device_id=trap.id,
        )
        assert trap_deployment.sampling_event == sampling_event
        assert trap_deployment.device == trap

        organism_capture = dt.OrganismCapture(
            organism_id=organism.id,
            deployment_id=trap_deployment.id,
        )
        assert organism_capture.deployment == trap_deployment
        assert organism_capture.organism == organism

        item = dt.Item(
            path="bla",
            site_id=site.id,
            device_id=device.id,
            sampling_event_id=sampling_event.id,
            organism_id=organism.id,
            organism_capture_id=organism_capture.id,
        )
        assert item.site == site
        assert item.device == device
        assert item.sampling_event == sampling_event
        assert item.organism == organism
        assert item.organism_capture == organism_capture

        annotation = dt.UserAnnotation(
            item_id=item.id,
            labels=[species, family],
        )
        assert annotation.item == item

    assert col.item.count() == 1
    assert col.userannotation.count() == 1
    assert col.organismcapture.count() == 1
    assert col.deployment.count() == 1
    assert col.samplingevent.count() == 2
    assert col.organism.count() == 1
    assert col.device.count() == 2
    assert col.site.count() == 2
    assert col.term.count() == 2


def test_dump_and_load(tmp_path):
    col = Collection()

    with col:
        family = dt.Term(
            value="Family 1",
            term_type="Family",
        )
        species = dt.Term(
            value="Species 1",
            term_type="Species",
            parent_id=family.id,
        )
        supersite = dt.Site(
            geometry=geom.Polygon(
                exterior=[
                    geom.Point(-1, -1),
                    geom.Point(-1, 1),
                    geom.Point(1, 1),
                    geom.Point(1, -1),
                ]
            ),
        )
        site = dt.Site(
            geometry=geom.Point(x=0, y=0),
            parent_id=supersite.id,
        )
        device = dt.Device(
            device_type="Recorder",
            model="Audiomoth",
        )
        trap = dt.Device(device_type="Bat Trap")
        super_sampling_event = dt.SamplingEvent(
            site_id=supersite.id,
            started_on=datetime.datetime.now() - datetime.timedelta(days=30),
            ended_on=datetime.datetime.now(),
        )
        sampling_event = dt.SamplingEvent(
            site_id=site.id,
            started_on=datetime.datetime.now() - datetime.timedelta(days=30),
            ended_on=datetime.datetime.now(),
            parent_id=super_sampling_event.id,
        )
        organism = dt.Organism(
            name="bat 1",
            organism_type="bat",
            labels=[
                species,
                family,
            ],
        )
        trap_deployment = dt.Deployment(
            sampling_event_id=sampling_event.id,
            deployed_on=sampling_event.started_on,
            recovered_on=sampling_event.ended_on,
            device_id=trap.id,
        )
        organism_capture = dt.OrganismCapture(
            organism_id=organism.id,
            deployment_id=trap_deployment.id,
        )
        item = dt.Item(
            path="bla",
            site_id=site.id,
            device_id=device.id,
            sampling_event_id=sampling_event.id,
            organism_id=organism.id,
            organism_capture_id=organism_capture.id,
        )
        dt.UserAnnotation(
            item_id=item.id,
            labels=[species, family],
        )

    col.dump(tmp_path)
    assert os.path.exists(tmp_path / "collection.json")

    fields = [
        "UserAnnotation",
        "Prediction",
        "Deployment",
        "Device",
        "EventType",
        "Item",
        "Organism",
        "OrganismCapture",
        "SamplingEvent",
        "Site",
        "Term",
    ]

    for field in fields:
        assert os.path.exists(tmp_path / f"{field}.json")

    col2 = Collection.load(tmp_path)
    for field in fields:
        name = field.lower()
        assert getattr(col, name).count() == getattr(col2, name).count()

    for field in fields:
        name = field.lower()
        store = getattr(col, name)
        model = getattr(dt, field)

        for obj in store:
            assert isinstance(obj, model)
