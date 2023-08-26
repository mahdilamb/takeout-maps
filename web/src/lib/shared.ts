/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type Id = number;
export type Start = string;
export type End = string;
export type Type =
	| 'BOATING'
	| 'CATCHING_POKEMON'
	| 'CYCLING'
	| 'FLYING'
	| 'HIKING'
	| 'HORSEBACK_RIDING'
	| 'IN_BUS'
	| 'IN_CABLECAR'
	| 'IN_FERRY'
	| 'IN_FUNICULAR'
	| 'IN_GONDOLA_LIFT'
	| 'IN_PASSENGER_VEHICLE'
	| 'IN_SUBWAY'
	| 'IN_TAXI'
	| 'IN_TRAIN'
	| 'IN_TRAM'
	| 'IN_VEHICLE'
	| 'IN_WHEELCHAIR'
	| 'KAYAKING'
	| 'KITESURFING'
	| 'MOTORCYCLING'
	| 'PARAGLIDING'
	| 'ROWING'
	| 'RUNNING'
	| 'SAILING'
	| 'SKATEBOARDING'
	| 'SKATING'
	| 'SKIING'
	| 'SLEDDING'
	| 'SNOWBOARDING'
	| 'SNOWMOBILE'
	| 'SNOWSHOEING'
	| 'STILL'
	| 'SURFING'
	| 'SWIMMING'
	| 'UNKNOWN_ACTIVITY_TYPE'
	| 'WALKING'
	| 'WALKING_NORDIC';
export type Id1 = number;
export type Start1 = string;
export type End1 = string;
export type Type1 =
	| 'BOATING'
	| 'CATCHING_POKEMON'
	| 'CYCLING'
	| 'FLYING'
	| 'HIKING'
	| 'HORSEBACK_RIDING'
	| 'IN_BUS'
	| 'IN_CABLECAR'
	| 'IN_FERRY'
	| 'IN_FUNICULAR'
	| 'IN_GONDOLA_LIFT'
	| 'IN_PASSENGER_VEHICLE'
	| 'IN_SUBWAY'
	| 'IN_TAXI'
	| 'IN_TRAIN'
	| 'IN_TRAM'
	| 'IN_VEHICLE'
	| 'IN_WHEELCHAIR'
	| 'KAYAKING'
	| 'KITESURFING'
	| 'MOTORCYCLING'
	| 'PARAGLIDING'
	| 'ROWING'
	| 'RUNNING'
	| 'SAILING'
	| 'SKATEBOARDING'
	| 'SKATING'
	| 'SKIING'
	| 'SLEDDING'
	| 'SNOWBOARDING'
	| 'SNOWMOBILE'
	| 'SNOWSHOEING'
	| 'STILL'
	| 'SURFING'
	| 'SWIMMING'
	| 'UNKNOWN_ACTIVITY_TYPE'
	| 'WALKING'
	| 'WALKING_NORDIC';
export type Name = string;
export type Path = string;
export type Icon = string | null;
export type Url = string | null;
export type Connected = boolean | null;
export type Label = string;
export type Path1 = string;
export type GroupBy = string | null;
export type ColorBy = string | null;
export type ColorMap1 = Categorical | Linear | Linear[] | null;
export type Dmin = number | string | null;
export type Dmax = number | string | null;
export type Min = string | null;
export type Max = string | null;
export type Color = string;
export type Layers = Layer[];
export type Metadata = BaseModel;
export type Data = BaseModel[];
export type Start2 = string | null;
export type End2 = string | null;
export type Type2 =
	| (
			| 'BOATING'
			| 'CATCHING_POKEMON'
			| 'CYCLING'
			| 'FLYING'
			| 'HIKING'
			| 'HORSEBACK_RIDING'
			| 'IN_BUS'
			| 'IN_CABLECAR'
			| 'IN_FERRY'
			| 'IN_FUNICULAR'
			| 'IN_GONDOLA_LIFT'
			| 'IN_PASSENGER_VEHICLE'
			| 'IN_SUBWAY'
			| 'IN_TAXI'
			| 'IN_TRAIN'
			| 'IN_TRAM'
			| 'IN_VEHICLE'
			| 'IN_WHEELCHAIR'
			| 'KAYAKING'
			| 'KITESURFING'
			| 'MOTORCYCLING'
			| 'PARAGLIDING'
			| 'ROWING'
			| 'RUNNING'
			| 'SAILING'
			| 'SKATEBOARDING'
			| 'SKATING'
			| 'SKIING'
			| 'SLEDDING'
			| 'SNOWBOARDING'
			| 'SNOWMOBILE'
			| 'SNOWSHOEING'
			| 'STILL'
			| 'SURFING'
			| 'SWIMMING'
			| 'UNKNOWN_ACTIVITY_TYPE'
			| 'WALKING'
			| 'WALKING_NORDIC'
	  )
	| null;
export type Id2 = number | null;
export type Errormessage = string;
export type Errorid = 'date-out-of-range';
export type Start3 = string;
export type End3 = string;
export type Value = number;
export type Min1 = number;
export type Max1 = number;
export type Months = [unknown, unknown][];
export type Latitude = number;
export type Longitude = number;
export type Altitude = number | null;
export type Accuracy = number | null;
export type Timestamp = string;
export type Locations = Location[];
export type Start4 = string;
export type End4 = string;
export type Min2 = number;
export type Max2 = number;
export type Start5 = string;
export type End5 = string;
export type Value1 = number;

export interface Activity {
	id: Id1;
	start: Start1;
	end: End1;
	type: Type1;
}
export interface Categorical {
	color_map: ColorMap;
}
export interface ColorMap {
	[k: string]: string;
}
export interface Connection {
	name: Name;
	path: Path;
	icon: Icon;
	url: Url;
	connected: Connected;
	layers: Layers;
}
export interface Layer {
	label: Label;
	path: Path1;
	group_by?: GroupBy;
	color_by?: ColorBy;
	color_map?: ColorMap1;
	color: Color;
}
export interface Linear {
	dmin?: Dmin;
	dmax?: Dmax;
	min: Min;
	max: Max;
}
export interface Dataset {
	metadata?: Metadata;
	data: Data;
	start?: Start2;
	end?: End2;
}
/**
 * Usage docs: https://docs.pydantic.dev/2.2/usage/models/
 *
 *     A base class for creating Pydantic models.
 *
 *     Attributes:
 *         __class_vars__: The names of classvars defined on the model.
 *         __private_attributes__: Metadata about the private attributes of the model.
 *         __signature__: The signature for instantiating the model.
 *
 *         __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *         __pydantic_core_schema__: The pydantic-core schema used to build the SchemaValidator and SchemaSerializer.
 *         __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *         __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *             This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *         __pydantic_generic_metadata__: Metadata for generic models; contains data used for a similar purpose to
 *             __args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
 *         __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *         __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *         __pydantic_root_model__: Whether the model is a `RootModel`.
 *         __pydantic_serializer__: The pydantic-core SchemaSerializer used to dump instances of the model.
 *         __pydantic_validator__: The pydantic-core SchemaValidator used to validate instances of the model.
 *
 *         __pydantic_extra__: An instance attribute with the values of extra fields from validation when
 *             `model_config['extra'] == 'allow'`.
 *         __pydantic_fields_set__: An instance attribute with the names of fields explicitly specified during validation.
 *         __pydantic_private__: Instance attribute with the values of private attributes set on the model instance.
 *
 */
export interface BaseModel {
	[k: string]: unknown;
}
export interface Event {
	type: Type2;
	id: Id2;
}
export interface ExceptionDetail {
	errorMessage: Errormessage;
	errorID: Errorid;
	[k: string]: unknown;
}
export interface Heartrate {
	start: Start3;
	end: End3;
	value: Value;
}
export interface HeartrateMetadata {
	zones: Zones;
}
export interface Zones {
	[k: string]: MinMaxInt;
}
export interface MinMaxInt {
	min: Min1;
	max: Max1;
	[k: string]: unknown;
}
export interface Histories {
	months: Months;
}
export interface Location {
	latitude: Latitude;
	longitude: Longitude;
	altitude?: Altitude;
	accuracy?: Accuracy;
	timestamp: Timestamp;
}
export interface LocationData {
	locations: Locations;
	start: Start4;
	end: End4;
}
export interface MinMax {
	min: Min2;
	max: Max2;
}
export interface Steps {
	start: Start5;
	end: End5;
	value: Value1;
}
