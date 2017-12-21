import React from 'react';
import { Text, View, TouchableOpacity, ActivityIndicator, StyleSheet} from 'react-native';
import { Camera, Permissions } from 'expo';
import { Button } from 'react-native-elements';
import PopupDialog, {ScaleAnimation,  DialogTitle} from 'react-native-popup-dialog';

const scaleAnimation = new ScaleAnimation();



export default class CameraExample extends React.Component {
  state = {
    hasCameraPermission: null,
    type: Camera.Constants.Type.back,
    ratio: '16:9',
    ratios: [],
    url: '',
    loadingAnimation: true,
    caption: ''
  };

  async componentWillMount() {

    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({ hasCameraPermission: status === 'granted' });
  }

   getRatios = async function() {
    const ratios = await this.camera.getSupportedRatios();
    return ratios;
  };

  setRatio(ratio) {
    this.setState({
      ratio,
    });
  }

 snap = async () => {
  if (this.camera) {
    let photo = await this.camera.takePictureAsync(); 
    console.log(photo.uri)
   
// **********
    let body = new FormData();

    body.append('photo', {uri: photo.uri, name: photo.uri, type:'image/jpg'});
    body.append('Content-Type','image/jpg');

    fetch("http://192.168.100.61:8000/main/",
      {
        method: 'POST', 
        headers: {
          "Content-Type": "multipart/form-data",
        },
        body:body
      }
    )
   /// .then((res) => checkStatus(res))
    .then((res) => res.json())
    .then((res) => {
                      console.log(res)
                      this.setState({caption: res, loadingAnimation: false})
                  })
    .catch((e) => console.log(e))
    .done()
// ************
  // this.setState({caption: photo.uri, loadingAnimation: false})
    
    // setInterval(() => {
    //   this.setState({
    //     loadingAnimation: !this.state.loadingAnimation
    //   });
    // }, 5000);


  }
  };

  render() {
    const { hasCameraPermission } = this.state;
    if (hasCameraPermission === null) {
      return <View />;
    } else if (hasCameraPermission === false) {
      return <Text>No access to camera</Text>;
    } else {
      return (
        <View style={{ flex: 1 }}>
          <Camera style={{
          flex: 1,
        }}  ref={ref => { this.camera = ref; }} type={this.state.type} ratio={this.state.ratio}>
            <View
              style={{
                flex: 1,
                backgroundColor: 'transparent',
                flexDirection: 'row',
                justifyContent: 'center'

              }}>
              <View style={{ alignSelf: 'flex-end', marginBottom: 10}}>
              <Button 
                 onPress={ () => {
                  this.setState({loadingAnimation: true})
                  this.snap();
                  this.popupDialog.show();

                 }}
                  large
                  raised
                  title='Take Picture'
                  backgroundColor='#397af8'
                  icon={{name: 'camera'}}
                style={{ alignSelf: 'flex-end', alignItems: 'center'}}
              />
              </View>

               <PopupDialog
                ref={(popupDialog) => { this.popupDialog = popupDialog; }}
                dialogAnimation={scaleAnimation}
                dialogTitle={<DialogTitle haveTitleBar={false} titleTextStyle={styles.resultTitle} title="Result" />}

                // dialogTitle={<DialogTitle title="Popup Dialog - Scale Animation" />}
                width = {0.75}
                dialogStyle={styles.popBox}
              >
                <View>
                { this.state.loadingAnimation
                  ? <ActivityIndicator size="large" color="#3E4348" />
                  : <Text style={styles.results}>{this.state.caption}</Text>
                }
                </View>
              </PopupDialog>
            </View>
          </Camera>
        </View>
      );
    }
  }
}


const styles = StyleSheet.create({
  popBox: {
    padding: 5,
    paddingRight:10,
    paddingLeft:10,
    backgroundColor: '#e1eef6'
  },
  results: {
    fontSize: 15,
    // fontWeight: 'bold',
    // margin: 10,
    color: '#282c37',
  },
  resultTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    // margin: 5
    color: '#004e66',
  }
});