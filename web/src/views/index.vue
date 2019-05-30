<style scoped lang="less">
	.index{
		width: 100%;
		margin: auto;
		text-align: center;
		font-size:30px;
		h1{
			height: 150px;
			color: white;
			img{
				height: 100%;
			}
		}
		h2{
			color: #666;
			margin-bottom: 200px;
			p{
				margin: 0 0 50px;
			}
		}
		.ivu-row-flex{
			height: 100%;
		}
	}
</style>
<template>
	<div class="index">
		<Layout>
        <Header><h1>Air Conditioner Client</h1></Header>
        <Content>
        	<Row type="flex" justify="center" align="middle">
				<Col span="10">
					<Form :model="formItem" :label-width="80">
						<FormItem label="Switch">
							<Button @click="powerOn">开机</Button>
							<Button @click="powerOff">关机</Button>
						</FormItem>
						<FormItem label="Room Id">
							<Input v-model="formItem.roomId" placeholder="Enter something..."></Input>
						</FormItem>
						<FormItem label="Target temperature">
							<Icon type="ios-thermometer" />
							<InputNumber :max="100" v-model="formItem.targetTenp"></InputNumber>℃
						</FormItem>
						<FormItem label="Mode">
							<RadioGroup v-model="formItem.mode" type="button">
								<Radio label="cool"></Radio>
								<Radio label="warm"></Radio>
							</RadioGroup>
						</FormItem>
						<FormItem label="Target wind speed">
							<RadioGroup v-model="formItem.wind" type="button">
								<Radio label="high"></Radio>
								<Radio label="medium"></Radio>
								<Radio label="low"></Radio>
							</RadioGroup>
						</FormItem>
						<FormItem>
							<Button type="primary" @click="submitSetting">Submit</Button>
						</FormItem>
					</Form>
				</Col>
				<Col span="6">
					
				</Col>
				<Col span="8">
					<Table :columns="tbcolumns" :data="tbdata"></Table>
				</Col>
			</Row>
        </Content>
        <Footer>Powered by group D.</Footer>
    	</Layout>

		
	</div>
</template>
<script>
	export default {
		data() {
			return {
				formItem: {
					roomId: "123",
					switch: "open",
					targetTenp: 20,
					mode: "cool",
					wind: "low"
				},
				nowState: {
					state: 'close',
					temperature: '20',
					wind_speed: 'low',
					energy: 0,
					fee: 0
				},
				tbcolumns: [
					{
						title: 'Item',
						key: 'item'
					},
					{
						title: 'Data',
						key: 'data'
					}
				]
			}
		},
		created: function(){
			this.initWebSocket();
		},
		mounted: function(){
			var timeUnit = 1000;
			this.timer = setInterval(this.tempSim, timeUnit);
		},
		destoryed: function(){
			this.websocketclose();
		},
		computed: {
			tbdata: function(){
				return [
				{
					item: 'state', 
					data: this.nowState.state
				},
				{
					item: 'temperature', 
					data: this.nowState.temperature + '℃'
				},
				{
					item: 'wind speed', 
					data: this.nowState.wind_speed
				},
				{
					item: 'energy', 
					data: this.nowState.energy
				},
				{
					item: 'fee', 
					data: this.nowState.fee
				}
				]
			}
		},
		methods: {
			tempSim(){
				defaultTemp = 25;
				delta = (this.nowState.temperature - defaultTemp) / 2;
				this.nowState.temperature -= delta;
				wind_speed = this.nowState.wind_speed;
				if(this.nowState.state == "ok"){
					if(this.formItem.mode == "cool"){
						this.nowState.temperature -= wind_speed;
					}else{
						this.nowState.temperature += wind_speed;
					}
				}
				 
			},
			powerOn(){
				let sendData = {
					"poweron": {
						"room_id": this.formItem.roomId,
						"cur_temp": this.nowState.temperature
					}
				};
				this.websocketsend(sendData);
			},
			powerOff(){
				let sendData = {
					"poweroff": {
						"room_id": this.formItem.roomId,
						"state": this.nowState.state
					} //开机or待机
				};
				this.websocketsend(sendData);
			},
			sendTemp(){
				let sendData = {
					"temp_update": {
						"room_id": this.formItem.roomId,
						"cur_temp": this.nowState.temperature
					}
				};
				this.websocketsend(sendData);
			},
			submitSetting(){
				let sendData =  {"config": {
										"room_id": this.formItem.roomId,
										"fan": this.formItem.wind_speed,
										"mode": this.formItem.mode,
										"target_temp": this.formItem.targetTenp
								}};
				this.websocketsend(sendData);
			},
			initWebSocket(){ //初始化weosocket 
				const wsuri = "ws://206.189.215.142:3000";//ws地址
				this.websock = new WebSocket(wsuri); 
				this.websock.onopen = this.websocketonopen;
				this.websock.onerror = this.websocketonerror;
				this.websock.onmessage = this.websocketonmessage; 
				this.websock.onclose = this.websocketclose;
		   }, 
		　　websocketonopen() {
			console.log("WebSocket连接成功");
		　　},
		　　websocketonerror(e) { //错误
			console.log("WebSocket连接发生错误");
		　　},
		　　websocketonmessage(e){ //数据接收 
			　//注意：长连接我们是后台直接1秒推送一条数据， 
			  //但是点击某个列表时，会发送给后台一个标识，后台根据此标识返回相对应的数据，
		  //这个时候数据就只能从一个出口出，所以让后台加了一个键，例如键为1时，是每隔1秒推送的数据，为2时是发送标识后再推送的数据，以作区分
			let data = e.data;
			let key = Object.keys(data)[0];
			switch(key){
				case 'poweron':
					this.nowState.state = data.poweron;
					break;
				case 'poweroff':
					if(data.poweron == 'fail'){
						this.$Message.info('Power off fail, please retry.')
					}
					break;
				case 'config':
					if(data.poweron == 'ok'){
						this.$Message.info('Setting success!')
					}else{
						this.$Message.info('Setting fail, please retry.')
					}
					break;
				case 'finish':
					this.$Message.info('Achieve target temperature!')
					break;
				case 'cost':
					this.nowState.fee = data.poweron;
					break;
				case 'energy':
					this.nowState.energy = data.poweron;
					break;
			}
		　　}, 
		　　websocketsend(dataObj){//数据发送 
				dataJoson = JSON.stringify(dataObj);
				console.log(dataJoson);
				this.websock.send(dataJoson); 
		　　}, 
		　 websocketclose(e){ //关闭 
			console.log("connection closed (" + e.code + ")"); 
		　　}
			
		}
	}
</script>
