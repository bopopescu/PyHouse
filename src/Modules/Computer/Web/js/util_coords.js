/**
 * @name:      PyHouse/src/Modules/Web/js/util_coords.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2016-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Sep 07, 2016
 * @summary:   Handles coordinates in JS
 *
 * Room coordinates are a list of three real values.
 * They are X, Y and Z or Easting, Northing and Height
 * They are in Meteres.
 */


function createCoordinates(self){
	X_Easting = 0.0;
	Y_Northing = 0.0;
	Z_Height = 0.0;
	var l_ret = [X_Easting, Y_Northing, Z_Height]
	return l_ret;
}

function buildCoordinatesEntry(self, p_coords, p_html) {
	p_html += buildCoordinatesWidget(self, 'RoomCoords', 'RoomCoords', p_coords);
	return p_html;
}

function buildCoordinatesWidget(self, p_id, p_caption, p_value) {
	// @param: p_id is the JS Id of the field.
	// @param: p_caption is the text to be put in front of the value field.
	// @param: p_value is the initial value of the coordinates (list of reals)
	// @returns: HTML for a coordinate entry.
	var l_id = buildAthenaId(self, p_id);
	var l_size = 40;
	var l_value = '';
	l_value = '[ ';
	l_value += _putFloat(p_value[0]) + ', ';
	l_value += _putFloat(p_value[1]) + ', ';
	l_value += _putFloat(p_value[2]);
	l_value += ' ]';
	var l_html = buildTopDivs(p_caption);
	l_html += "<input type='text' class='lcars-button-addition'";
	l_html += setIdAttribute(l_id);
	l_html += setSizeAttribute(l_size);
	l_html += setValueAttribute(l_value);
	l_html += " />\n";
	l_html += buildBottomDivs();
	return l_html;
}

function createCoordinatesEntry(self, p_data) {
	p_data.RoomCoords = self.createCoordinates();
	return p_data;
}

function fetchCoordinateEntry(self, p_data) {
	p_data.RoomCoords = fetchCoordinatesWidget(self, 'RoomCoords');
	return p_data;
}

function fetchCoordinatesWidget(self, p_id) {
	// Divmod.debug('---', 'util_coords.fetchCoordinatesWidget() was called.');
	var l_coords = self.nodeById(p_id).value;
	l_vals = l_coords.replace('[','').replace(' ', '').split(',');
	// console.log("util_coords.fetchCoordinatesWidget() - %O", l_vals);
	var l_x = parseFloat(l_vals[0]);
	var l_y = parseFloat(l_vals[1]);
	var l_z = parseFloat(l_vals[2]);
	var l_ret = [l_x, l_y, l_z];
	// console.log("util_coords.fetchCoordinatesWidget() - %O", l_ret);
	// Divmod.debug('---', 'util_coords.fetchCoordinatesWidget() called.  FinalValue=' + l_ret);
	return l_ret;
}


// Divmod.debug('---', 'util_coords.buildSerialPart() called.');
// console.log("util_coords.handleMenuOnClick() - l_obj = %O", l_obj);
// ### END DBK
