<template>
    <div>
        <v-select class = "player-selection" label="Player 1" :items="non_ai_agent_players" v-model="selected" outlined/>
        <v-select class = "player-selection" label="Player 2" :items="players" v-model="selected2" :disabled="selected === null" outlined/>
        <h3>AI Agent Attributes</h3>
        <br>
        <v-text-field class="ai-agent-attrs" value="90" label="AI Agent Turn Timeout (Seconds)" :disabled="isDisabled" v_model="agent_timeout"></v-text-field>
        <v-select class = "ai-agent-attrs" label="AI Agent Playing Strategy" :items="ai_strategies" v-model="ai_agent_strategy" :disabled="isDisabled" outlined/>
        <div>
            <v-btn @click="on_player_select()" color="primary" large :disabled="selected2 === null" >Start Game</v-btn>
        </div>
        <br>
        <div>
            <v-btn @click="reloadPage" color="primary" large :disabled="selected2 === null" >Reset Game</v-btn>
        </div>

    </div>
</template>
<style id="player-selector-style-file">
    .player-selection {
        width: 50%;
    }
    .ai-agent-attrs {
        width: 50%;
    }
</style>
<script>
    module.exports = {
        methods: {
            reloadPage() {
                window.location.reload();
            },
    },
    watch: {
        selected2: function(newVal) {
            console.log(this.ai_agent_vals.includes(newVal));
            if (this.ai_agent_vals.includes(newVal)) {
                this.isDisabled = false;
            } else {
                this.isDisabled = true;
            }
        },
    },
};
</script>